var ZipCode = {
  /**
  * содержит JSON объекта содержащего адреса для данного почтового кода
  */
  adds: null,
  complete: false,
  /**
  * получает JSON объекта содержащего адреса для данного почтового кода
  */
  fetchAdds: function(zip, callback){
    ZipCode.complete = false;
    $.ajax({
      type: 'GET',
      url: 'http://zip.wab-net.ru/zipp/{0}'.format(zip),
      dataType: 'jsonp',
      jsonpCallback: 'successCallback',
      success: function(data) {
        ZipCode.adds = data.zip;
        ZipCode.complete = true;
        callback();
      }
    });
  },
  items: function(){
    var keys = new Array();
    var vals = new Array();
    var names = new Array();
    var len = 0;
    for (var key in ZipCode.adds.subject) {
      keys.push(key);
      vals.push(ZipCode.adds.subject[key]);
      names.push('{0} {1}'.format(ZipCode.adds.subject[key].socr, ZipCode.adds.subject[key].name));
      len++;
    }
    return {'length': len, 'keys': keys, 'values': vals, 'names': names};
  },
  subject: function(subject){
    var subject = ZipCode.adds.subject[subject]
    return {
      name: '{0} {1}'.format(subject.socr, subject.name),
      items: function() {
        var keys = new Array();
        var vals = new Array();
        var names = new Array();
        var len = 0;
        for (var key in subject.county) {
          keys.push(key);
          vals.push(subject.county[key]);
          names.push('{0} {1}'.format(subject.county[key].socr, subject.county[key].name));
          len++;
        }
        return {'length': len, 'keys': keys, 'values': vals, 'names': names};
      },
      county: function(county) {
        var county = subject.county[county];
        return {
          name: '{0} {1}'.format(county.socr, county.name),
          items: function() {
            var keys = new Array();
            var vals = new Array();
            var names = new Array();
            var len = 0;
            for (var key in county.city) {
              keys.push(key);
              vals.push(county.city[key]);
              names.push('{0} {1}'.format(county.city[key].socr, county.city[key].name));
              len++;
            }
            return {'length': len, 'keys': keys, 'values': vals, 'names': names};
          },
          city: function(city) {
            var city = county.city[city];
            return {
              name: '{0} {1}'.format(city.socr, city.name),
              items: function() {
                var keys = new Array();
                var vals = new Array();
                var names = new Array();
                var len = 0;
                for (var key in city.place) {
                  keys.push(key);
                  vals.push(city.place[key]);
                  names.push('{0} {1}'.format(city.place[key].socr, city.place[key].name));
                  len++;
                }
                return {'length': len, 'keys': keys, 'values': vals, 'names': names};
              },
              place: function(place) {
                var place = city.place[place];
                return {
                  name: '{0} {1}'.format(place.socr, place.name),
                  items: function() {
                    var keys = new Array();
                    var vals = new Array();
                    var names = new Array();
                    var len = 0;
                    for (var key in place.street) {
                      keys.push(key);
                      vals.push(place.street[key]);
                      names.push('{0} {1}'.format(place.street[key].socr, place.street[key].name));
                      len++;
                    }
                    return {'length': len, 'keys': keys, 'values': vals, 'names': names};
                  },
                  street: function(street) {
                    var street = place.street[street];
                    return {
                      name: '{0} {1}'.format(street.socr, street.name),
                      items: function() {
                        var keys = new Array();
                        var vals = new Array();
                        var names = new Array();
                        var len = 0;
                        for (var key in street.house) {
                          keys.push(key);
                          vals.push(street.house[key]);
                          names.push('{0} {1}'.format(street.house[key].socr, street.house[key].name));
                          len++;
                        }
                        return {'length': len, 'keys': keys, 'values': vals, 'names': names};
                      },
                      house: function(house) {
                        var house = street.house[house];
                        return {
                          name: '{0} {1}'.format(house.socr, house.name)
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}

