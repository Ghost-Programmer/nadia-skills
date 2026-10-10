---
name: NetworkSkill
description: Instructions on how to scan local subnets, resolve DNS hosts, trace routing hops, geolocate hosts, resolve MAC addresses and vendors, discover 2D and 3D network printers, check live printing status, and perform WHOIS lookups.
tools: [getNetworkTopology, traceRoute, getNodeDetails, scanPorts, grabBanner, getGeoLocation, whoisLookup, dnsLookup, dnsResolve, dnsReverseLookup, getMacAddress, getMacVendor, syncMacVendors, scanForPrinters, getPrinterLiveStats]
---
# Network Diagnostics, DNS, and Scanning Guidelines

Use this skill when you need to resolve hostnames, query DNS records, run WHOIS domain ownership diagnostics, perform network scans, port scanning, trace routing hops, grab service banners, look up or synchronize MAC vendor hardware databases, scan for 2D and 3D network printers, inspect real-time printing jobs and toner levels, or determine the physical location of public IP addresses.

## Guidelines

1. **Local Network Topology Discovery (`getNetworkTopology`)**:
   - Invoke this tool when asked to list active hosts on the subnet, check local adapter configurations, default gateway, or local DNS servers.
   - It runs a ping sweep and extracts the ARP cache to identify active local IPs.

2. **Traceroute Routing Hop Map (`traceRoute`)**:
   - Use `traceRoute` when diagnosing network packet paths, latency delays, or router hops to a remote target.
   - Specify the target IP address as the argument.

3. **Single Node Diagnostics (`getNodeDetails`)**:
   - Use this to resolve canonical hostnames and run a quick latency check (ping) on a target host IP.

4. **Port Scanning (`scanPorts`)**:
   - Use `scanPorts` to audit active TCP services on a host.
   - Set the `startPort` and `endPort` range carefully to avoid scanning too many ports (e.g., scan common ones like 1-1024, or specific targets like 22, 80, 443, 8080).
   - Use a sensible thread count (defaults to 20; can increase up to 50 for faster scans).

5. **Banner Grabbing (`grabBanner`)**:
   - Once an open port is identified, call `grabBanner` to read the initial service identification/header string, assisting in OS and daemon version detection.

6. **IP Geolocation (`getGeoLocation`)**:
   - Invoke `getGeoLocation` on public IP addresses to fetch latitude/longitude coordinates, city, and country details via IP-API.
   - Do not call this on private IP ranges (e.g., `192.168.x.x`, `10.x.x.x`, `127.0.0.1`), as public geolocation lookups will fail for them.

7. **WHOIS Lookups (`whoisLookup`)**:
   - Use `whoisLookup` to query domain registration, registrar info, and domain ownership details.
   - Specify the target domain name as the argument.

8. **DNS Record Queries (`dnsLookup`)**:
   - By default, run `dnsLookup` with the `recordType` set to "ALL" to gather a complete diagnostic profile of the domain.
   - If looking for a specific type (e.g., MX record for mail routing, TXT record for SPF/DKIM verification, SOA for authority details), specify it in the `recordType` parameter.
   - You can optionally specify a custom `dnsServer` (e.g., `8.8.8.8` or `1.1.1.1`) if the default system resolver is slow or returns incomplete data.

9. **Resolving Domains to IP Addresses (`dnsResolve`)**:
   - Use `dnsResolve` when you specifically need the raw IP addresses (IPv4 and IPv6) of a host.

10. **Reverse DNS Lookup (`dnsReverseLookup`)**:
    - Use `dnsReverseLookup` to find the canonical hostname (PTR record) of a given IP address.

11. **MAC Address Resolution (`getMacAddress`)**:
    - Use `getMacAddress` to look up the physical hardware MAC address and hardware vendor for a given IP address on the local network or host machine.

12. **MAC Vendor Lookup (`getMacVendor`)**:
    - Use `getMacVendor` to look up the equipment manufacturer/vendor for a specific MAC address (e.g. `00-11-22-33-44-55` or OUI prefix `00:11:22`).

13. **Synchronizing MAC Vendor Database (`syncMacVendors`)**:
    - Use `syncMacVendors` to download and update the local database with the latest official Nmap MAC prefixes dataset from GitHub.

14. **2D & 3D Network Printer Discovery (`scanForPrinters`)**:
    - Use `scanForPrinters` when asked to find printers on the local network.
    - Probes IPP (Port 631), JetDirect/RAW (Port 9100), LPD (Port 515), Bambu MQTT (Port 8883), and mDNS.
    - Returns active state (`isPrinting: true/false`, state: `PRINTING` / `IDLE`), current job or 3D print file, queued jobs count, ink/toner supply levels, 3D printer nozzle and bed temperatures, and hardware warnings (paper jam, low toner, door open).

15. **Printer Live Telemetry & Status Query (`getPrinterLiveStats`)**:
    - Use `getPrinterLiveStats` with a specific printer IP to check if it is currently printing, view ink/toner levels, check queued job counts, or monitor extruder temperatures.

## Setup Instructions

### 1. Prerequisites & Network Capabilities
- **Local Network Interfaces**: Host machine must have an active local network interface (Ethernet/Wi-Fi) connected to target subnets.
- **Port Permissions**: Banner grabbing, printer discovery (IPP 631, JetDirect 9100, LPD 515), WHOIS (port 43), and port scanning require unobstructed socket access.

### 2. MAC Vendor Database & External APIs
- **Nmap MAC Database**: The MAC vendor lookup tool references the local IEEE/Nmap prefix registry. Run `syncMacVendors` to refresh the local definitions file from upstream sources.
- **Geolocation API**: IP Geolocation utilizes public IP-API endpoints. Ensure outbound HTTP/HTTPS traffic is allowed.

