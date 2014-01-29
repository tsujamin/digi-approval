#!/bin/bash

which tmux || sudo yum install -y tmux

cd `dirname $0`/../..

tmux has-session -t digiapproval && tmux attach -t digiapproval || {
    tmux new-session -d -s digiapproval "scl enable python27 bash"
    for rcfile in src/dev/*.rc; do
        rcname=`basename $rcfile .rc`
        tmux new-window -t digiapproval -n $rcname "src/dev/spawn-scl.sh ${rcname}.rc"
    done
    for rcfile in src/dev/*.sudorc; do
        rcname=`basename $rcfile .sudorc`
        tmux new-window -t digiapproval -n $rcname "sudo src/dev/spawn-scl.sh ${rcname}.sudorc"
    done
    tmux attach -t digiapproval
}
