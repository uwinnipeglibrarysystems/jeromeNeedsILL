# Copyright (c) 2021 University of Winnipeg
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from ipaddress import ip_address, ip_network, IPv4Network, IPv6Network

def get_rule_if_ip_matches(ip, rules):
    ip_addr = ip_address(ip)
    ip_addr_net = ip_network(ip, strict=False)
    for rule_key, rule_value in rules:
        if rule_key == 'PRIVATE':
            if ip_addr.is_private:
                return rule_value
        elif rule_key == 'LOOPBACK':
            if ip_addr.is_loopback:
                return rule_value
        elif isinstance(rule_key, (IPv4Network, IPv6Network)):
            if rule_key.overlaps(ip_addr_net):
                return rule_value
        else:
            raise Exception(
                "ip address configuration matching rule is not one of the "
                "accepted values PRIVATE, LOOPBACK, or type "
                "ipaddress.IPv4Network or type ipaddress.IPv4Network"
            )
            
    return False

