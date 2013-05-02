# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import psycopg2


class ShinukUpdatePipeline(object):

  def ThingNotPresent(self, id):
    cur = self.conn.cursor()
    cur.execute("DELETE FROM goods_thing_size WHERE thing_id = %s;" % id)
    self.conn.commit()
    cur.execute("UPDATE goods_thing SET present = false WHERE id = %s;" % id)
    self.conn.commit()
    cur.close()
    return

  def ModelNotPresent(self, id):
    cur = self.conn.cursor()
    cur.execute("SELECT id FROM goods_thing WHERE model_id = %s;" % id)
    self.conn.commit()
    for rec in cur:
      self.ThingNotPresent(rec[0])
    cur.close()
    return

  def GetOrCreateSize(self, size, size_en):
    cur = self.conn.cursor()
    cur.execute("SELECT id FROM goods_size WHERE size = %s;" % size)
    self.conn.commit()
    result = cur.fetchone()
    if not result:
      cur.execute("INSERT INTO goods_size (size, size_en, size_ru) VALUES ('%s', '%s', '%s');" % (size, size_en, size_en))
      self.conn.commit()
      cur.execute("SELECT id FROM goods_size WHERE size = %s;" % size)
      self.conn.commit()
      result = cur.fetchone()
    cur.close()
    return result[0]

  def process_item(self, item, spider):
    self.conn = psycopg2.connect('dbname = shinuk user = shinuk')
    if not item['name']:
      self.ModelNotPresent(item['pk'])
      return item
    cur = self.conn.cursor()
    cur.execute("SELECT goods_color.name, goods_thing.id, present, price, oldprice FROM goods_thing INNER JOIN goods_color ON goods_color.id = goods_thing.color_id WHERE model_id = %s;" % item['pk'])
    self.conn.commit()
    for rec in cur:
      color, thing_id, pres, price, oldprice = rec
      try: 
#        print 'process model: %s, color: %s' % (item['art'], color)
        thing = item['items'][color]
        ispresent = False
        price = 0.0;
        oldprice = 0.0;
        cur2 = self.conn.cursor()
        # delete all sizes
        cur2.execute("DELETE FROM goods_thing_size WHERE thing_id = %s;" % thing_id)
        self.conn.commit()
        for i in thing:
          size = i['size']
          present = i['present']
          if present:
            # insert size
            size_id = self.GetOrCreateSize(size, i['size_en'])
            cur2.execute("INSERT INTO goods_thing_size (thing_id, size_id) VALUES ('%s', '%s');" % (thing_id, size_id))
            self.conn.commit()
            ispresent = True
            price = max(float(price), float(i['price']))
            oldprice = max(float(oldprice), float(i['oldprice']))
        # update present flag and prices
        if ispresent:
          cur2.execute("UPDATE goods_thing SET present = true, price = %s, oldprice = %s WHERE id = %s;" % (price, oldprice, thing_id))
          self.conn.commit()
        else:
          cur2.execute("UPDATE goods_thing SET present = false, price = %s, oldprice = %s WHERE id = %s;" % (price, oldprice, thing_id))
          self.conn.commit()
        cur2.close()
      except KeyError:
        # thing not present
        self.ThingNotPresent(thing_id)
    cur.close()
    self.conn.close()
    return item
