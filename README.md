
# Web Proxy Auto-Configurer Service

A service which scrapes a list of free web proxies from the internet, and re-formats the list into a [Proxy Auto Config](https://en.wikipedia.org/wiki/Proxy_auto-config) file which web browsers can understand.

### Purpose:
 - Working around Geo-blocked websites (or testing Geo-blocking works) for people who don't want to spend money.

### Non-goals:
 - Security/privacy. Its unclear who runs these things, and no information of any importance should be passed through them (login credentials, etc)
 - Testing that the proxy actually works - the upstream provider is assumed to have done that.
 - Performance will likely suffer badly. Find a paid VPN provider if this is required.

## API

`https://<BASE_URL>/proxies`

| Parameter  | Default Value | Description                                                                        |
|------------|---------------|------------------------------------------------------------------------------------| 
| country    | None          | 2 letter ISO country code the proxies are in                                       
| timeout | 500 | Millisecond timeout passed to list provider, to filter out slower proxies          |
| count | 3 | Number of proxies to return to the browser - useful if first proxy no longer works |
| whitelist | None | Instead of using the proxy for everything, only use it for specific websites. Can be specified multiple times |

Example:

`http://127.0.0.1:5000/proxies`

Response:

`function FindProxyForURL(url, host) { return 'SOCKS5 144.31.101.200:1080; SOCKS5 206.123.156.211:4550; SOCKS5 206.123.156.183:5166' ; }`

Example 2:

`http://127.0.0.1:5000/proxies?country=de&count=2&whitelist=blockedsite.com&whitelist=*.blockedsite.com`

Response 2:

`function FindProxyForURL(url, host) { if ( shExpMatch(host, 'blockedsite.com') || shExpMatch(host, '*.blockedsite.com') ) { return 'SOCKS5 91.99.182.39:4000; SOCKS5 85.190.99.143:443' ; } return 'DIRECT'; }`

## Using with a web browser

For Firefox:

(Menu) -> Settings -> General -> Network Settings

And then put in the URL in the "Automatic proxy configuration URL" box.

Other browsers should be similar.

## Disclaimer

Use at your own risk. I don't run the proxies either.

Some AI code was used in the commit history, but some may still remain.