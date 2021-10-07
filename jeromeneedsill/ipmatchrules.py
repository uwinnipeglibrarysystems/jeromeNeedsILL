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

