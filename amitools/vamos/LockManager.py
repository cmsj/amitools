from Log import log_lock
import os.path

class AmiLock:
  def __init__(self, ami_path, sys_path, exclusive):
    self.ami_path = ami_path
    self.sys_path = sys_path
    self.name = os.path.basename(sys_path)
    self.exclusive = exclusive
    self.addr = 0
    self.b_addr = 0
  def __str__(self):
    return "[Lock:'%s'(ami='%s',sys='%s',ex=%d)@%06x=b@%06x]" % (self.name, self.ami_path, self.sys_path, self.exclusive, self.addr, self.b_addr)

class LockManager:
  def __init__(self, path_mgr, base_addr):
    self.path_mgr = path_mgr
    self.base_addr = base_addr
    self.cur_addr = base_addr
    log_lock.info("init manager: base=%06x" % self.base_addr)
    self.locks_by_b_addr = {}
  
  def _register_lock(self, lock):
    addr = self.cur_addr
    self.cur_addr += 4
    lock.addr = addr
    lock.b_addr = addr >> 2
    self.locks_by_b_addr[lock.b_addr] = lock
    log_lock.info("registered: %s" % lock)
    
  def _unregister_lock(self, lock):
    check = self.locks_by_b_addr[lock.b_addr]
    if check != lock:
      raise ValueError("Invalud Lock unregistered: %s" % lock)
    del self.locks_by_b_addr[lock.b_addr]
    log_lock.info("unregistered: %s" % lock)
    lock.b_addr = 0
    lock.addr = 0
  
  def create_lock(self, ami_path, exclusive):
    if ami_path == '':
      return None
    sys_path = self.path_mgr.ami_to_sys_path(ami_path)
    if sys_path == None:
      log_lock.info("lock not found: '%s'" % ami_path)
      return None
    exists = os.path.exists(sys_path)
    if not exists:
      log_lock.info("lock not found: '%s' -> '%s'" % (ami_path, sys_path))
      return None      
    lock = AmiLock(ami_path, sys_path, exclusive)
    self._register_lock(lock)
    return lock
  
  def get_by_b_addr(self, b_addr):
    if self.locks_by_b_addr.has_key(b_addr):
      return self.locks_by_b_addr[b_addr]
    else:
      raise ValueError("Invalid File Lock at b@%06x" % b_addr)
  
  def release_lock(self, lock):
    self._unregister_lock(lock)

  def examine_lock(self, lock, fib_mem):
    name_addr = fib_mem.get_addr('fib_FileName')
    fib_mem.w_cstr(name_addr, lock.name)
    fib_mem.w_s('fib_DiskKey',0xcafebabe)
    if os.path.isdir(lock.name):
      dirEntryType = 0x01 # pos
    else:
      dirEntryType = 0xffffffff # neg
    fib_mem.w_s('fib_DirEntryType', dirEntryType )
    prot = 0xf
    fib_mem.w_s('fib_Protection', prot)
    if os.path.isfile(lock.sys_path):
      size = os.path.getsize(lock.name)
      fib_mem.w_s('fib_Size', size)
    
    