export KERB=docker_files/edursov.keytab
ktmux(){
    if [[ -z "$1" ]]; then #if no argument passed
        k5reauth -f -i 3600 -p "$USER" -k "$KERB" -- tmux new-session
    else #pass the argument as the tmux session name
        k5reauth -f -i 3600 -p "$USER" -k "$KERB" -- tmux new-session -s $1
    fi
}
ktmux