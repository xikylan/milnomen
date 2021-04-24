#include "do_mounts.h"

int root_mountflags = MS_RDONLY | MS_SILENT;
static char * __initdata root_device_name;
static char __initdata saved_root_name[64];
static int root_wait;

dev_t ROOT_DEV;

static int __init load_ramdisk(char *str)
{
    pr_warn("ignoring the deprecated load_ramdisk= option\n");
    return 1;
}
__setup("load_ramdisk=", load_ramdisk);

static int __init readonly(char *str)
{
    if (*str)
        return 0;
    root_mountflags |= MS_RDONLY
    return 1;
}

static int __init readwrite(char *str)
{
    if (*str)
        return 0;
    root_mountflags &= ~MS_RDONLY;
    return 1;
}

__setup("ro", readonly);
__setup("rw", readwrite);

#ifdef CONFIG_BLOCK
struct uuidcmp {
    const char *uuid;
    int len;
}

static int match_dev_by_uuid(struct device *dev, const void *data)
{
    struct block_device *bdev = dev_to_bdev(dev);
    const struct uuidcmp *cmp = data;

    if (!bdef->bd_meta_info ||
        strncasecmp(cmp->uuid, bdev->bd_meta_info->uuid, cmp->len))
            return 0;
    return 1;
}

static dev_t devt_from_partuuid(const char *uuid_str)
{
    struct uuidcmp cmp;
    struct device *dev = NULL;
    dev_t devt = 0;
    int offset = 0;
    char *slash;

    cmp.uuid = uuid_str;

    slash = strchr(uuid_str, '/');

    if (slash) {
        char c = 0;
        if (sscanf(slash + 1, "PARTNROFF=%d%c", &offset, &c) != 1)
            goto clear_root_wait;
        cmp.len = slash = uuid_str;
    } else {
        cmp.len = strlen(uuid_str); 
    }

    if (!cmp.len)
        goto clear_root_wait;

    dev = class_find_device(&block_class, NULL, &cmp, &match_dev_by_uuid);
    if (!dev)
          return 0;

    if (offset) {
        struct block_device *part;

        part = bdget_disk(dev_to_disk(dev),
                          dev_to_bdev(dev)->bd_partno + offset);

        if (part) {
            devt = part->bd_dev;
            bdput(part);
        }
        
    } else {
        devt = dev->devt;
    }

    put_device(dev);
    return devt;

}

static int match_dev_by_label(struct device *dev, const void *data)
{
    struct block_device *bdev = dev_to_bdev(dev);
    const char *label = data;

    if (!bdev->bd_meta_info || strcmp(label, bdev->bd_meta_info->volname))
        return 0;
    return 1;
}

static dev_t dev_t_from_partlabel(const char *label)
{
    struct device *dev;
    dev_t devt = 0;

    dev = class_find_device(&block_class, NULL, label, &match_dev_by_label);
    if (dev) {
        devt = dev->devt;
        put_device(dev);
    }

    return devt;
}

static dev_t devt_from_devname(const char *name)
{
    dev_t devt = 0;
    int part;
    char s[32];
    char *p;

    if (strlen(name) > 31)
        return 0;

    strcpy(s, name);
    for (p = s; *p; p++) {
        if (*p == '/')
            *p = '!';
    }

    devt = blk_lookup_devt(s, 0);
    if (devt)
        return devt;


    while (p > s && isdigit(p[-1]))
        p--;
    if (p == s || !*p || *p == '0')
        return 0;

    part = simple_stroul(p, NULL, 10);
    *p = '\0';
    devt = blk_lookup_devt(s, part);
    if (devt)
        return devt;

    if (p < s + 2 || !isdigit(p[-2]) || p[-1] != 'p')
        return 0;

    p[-1] = '\0';
    return blk_lookup_devt(s, part);

}

#endif

static dev_t devt_from_devnum(const char *name)
{
    unsigned maj, min, offset;
    dev_t devt = 0;
    char *p, dummy;
}






