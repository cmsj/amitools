#!/bin/sh

DISK="/dev/rdisk6"
TOOL="./rdbtool"

${TOOL} ${DISK} init rdb_cyls=8

${TOOL} ${DISK} fsadd ~cmsj/Downloads/A600/pfs3_aio-handler dostype=0x50465303

${TOOL} ${DISK} add size=100MiB name=DH0 fs=0x50465303 automount=true bootable=true max_transfer=0x1fe00
${TOOL} ${DISK} add size=500MiB name=DH1 fs=0x50465303 automount=true max_transfer=0x1fe00
${TOOL} ${DISK} add size=1GiB name=DH2 fs=0x50465303 automount=true max_transfer=0x1fe00
${TOOL} ${DISK} fill name=DH3 fs=0x50465303 automount=true max_transfer=0x1fe00
${TOOL} ${DISK} change 3 max_transfer=0x1fe00

${TOOL} ${DISK} map
${TOOL} ${DISK} info
