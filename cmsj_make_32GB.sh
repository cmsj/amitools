#!/bin/sh
set -eux

OUTFILE="32GB.hdf"
RDBTOOL="./rdbtool"

rdbtool() {
  "${RDBTOOL}" "${OUTFILE}" "$@"
}

rdbtool create chs=1953125,1,32
rdbtool init rdb_cyls=8
rdbtool info
rdbtool fsadd ~/Downloads/A600/pfs3_aio-handler dostype=0x50465303
rdbtool add size=512MiB name=DH0 fs=0x50465303 automount=true bootable=true max_transfer=0x1fe00
rdbtool add size=5GiB name=DH1 fs=0x50465303 automount=true
rdbtool add size=10GiB name=DH2 fs=0x50465303 automount=true
rdbtool fill name=DH3 fs=0x50465303 automount=true
rdbtool map
rdbtool info
