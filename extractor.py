#!/usr/bin/env python3

import dns.resolver
import requests
from urllib.parse import urljoin

def dns_lookup(domain):
    try:
        # Perform DNS A record lookup for the domain
        answers = dns.resolver.resolve(domain, 'A')
        
        # Extract IP addresses from the answers
        ip_addresses = [answer.address for answer in answers]
        
        return ip_addresses
    except dns.resolver.NoAnswer:
        return "No A records found for the domain."
    except dns.resolver.NXDOMAIN:
        return "Domain does not exist."
    except dns.exception.Timeout:
        return "DNS lookup timed out."
    except Exception as e:
        return f"An error occurred: {e}"

def check_robots_txt(domain):
    try:
        # Construct the URL for the robots.txt file
        url = f"http://{domain}/robots.txt"
        
        # Send a GET request to fetch the robots.txt file
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.text
        elif response.status_code == 404:
            return "robots.txt file not found."
        else:
            return f"Failed to retrieve robots.txt: HTTP {response.status_code}"
    
    except requests.RequestException as e:
        return f"Error fetching robots.txt: {e}"

def directory_enumeration(domain):
    common_directories = ['admin', 'wp-admin', 'login', 'wp-login.php', 'administrator', 'phpmyadmin', 'backup']
    results = []
    
    for directory in common_directories:
        url = f"http://{domain}/{directory}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                results.append(f"Found: {url}")
            elif response.status_code == 403:
                results.append(f"Forbidden: {url}")
            elif response.status_code == 401:
                results.append(f"Unauthorized: {url}")
        
        except requests.RequestException:
            pass
    
    return results

if __name__ == "__main__":
    domain_name = input("Enter the domain name: ")
    
    # Perform DNS lookup
    ips = dns_lookup(domain_name)
    print(f"IP addresses for {domain_name}:")
    if isinstance(ips, list):
        for ip in ips:
            print(ip)
    else:
        print(ips)
    
    print("\nChecking robots.txt file:")
    robots_txt_content = check_robots_txt(domain_name)
    print(robots_txt_content)
    
    print("\nPerforming directory enumeration:")
    directory_results = directory_enumeration(domain_name)
    for result in directory_results:
        print(result)
