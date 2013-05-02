# Scrapy settings for shinuk_update project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'shinuk_update'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['shinuk_update.spiders']
NEWSPIDER_MODULE = 'shinuk_update.spiders'
DEFAULT_ITEM_CLASS = 'shinuk_update.items.ShinukUpdateItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
ITEM_PIPELINES = [
    'shinuk_update.pipelines.ShinukUpdatePipeline',
]
