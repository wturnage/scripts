{% for fqdn, hostname in salt['mine.get']('*', 'network.get_hostname', expr_form='glob').items() %}

nagios minion config:
  file.managed:
    - name: /usr/local/nagios/etc/conf.d/servers/{{ hostname }}.cfg
    - source: salt://app_vu/nagios/files/minions.cfg
    - user: nagios
    - group: nagios
    - mode: 664
    - template: jinja
    - replace: False

{% endfor %}
~                                                             
