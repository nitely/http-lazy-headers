# HTTP Lazy Headers

> This is in active development and it's not stable at all. Check it back later.

HLH is an abstraction over raw HTTP headers, providing:

* Lazy decoding, parsing and validation of input headers
* Eager validation and lazy formatting of output headers
* Methods and helpers for common operations
* A headers collection on top of `OrderedDict` for fast lookups
* WSGI support
* A pure Python implementation without using regex!
* A sane API
* A way out of messy strings manipulation and typos


## Compatibility

* Python +3.5


## Install

```
$ pip install http_lazy_headers
```


## Usage

Input headers:

```python
import http_lazy_headers as hlh


accept = hlh.Accept(
    raw_values_collection=[
        'foo/bar;baz=qux, */*;q=0.5'])

accept.values()
# (
#     (('foo', 'bar'), ParamsCI((('baz', 'qux'),))),
#     (('*', '*'), ParamsCI((('q', 0.5),)))
# )
```

Output headers:

```python
import http_lazy_headers as hlh


headers = hlh.HeadersMut()

headers.set(
    hlh.Accept([
        hlh.accept(
            hlh.MediaType.text,
            hlh.MediaType.html,
            quality=1),
        hlh.accept(
            hlh.MediaType.text,
            hlh.MediaType.star,
            quality=0.5)]))

headers.set(
    hlh.Host([
        hlh.host('www.Alliancefrançaise.nu')]))

headers.set(
    hlh.Connection([
        hlh.ConnectionOptions.keep_alive]))

str(headers)
# ('accept: text/html;q=1, text/*;q=0.5\r\n'
#  'host: xn--www.alliancefranaise.nu-dbc\r\n'
#  'connection: keep-alive')
```

More -> [docs]()


## Specs. Support

* [rfc7230](http://httpwg.org/specs/rfc7230.html)
* [rfc7231](http://httpwg.org/specs/rfc7231.html)
* [rfc7232](http://httpwg.org/specs/rfc7232.html)
* [rfc7233](http://httpwg.org/specs/rfc7233.html)
* [rfc7234](http://httpwg.org/specs/rfc7234.html)
* [rfc7235](http://httpwg.org/specs/rfc7235.html)
* [rfc6265](http://httpwg.org/specs/rfc6265.html)
* [rfc3986](https://tools.ietf.org/html/rfc3986) for `Host` validation.
* [rfc5646](https://tools.ietf.org/html/rfc5646)
* [rfc6266](https://tools.ietf.org/html/rfc6266)
* [rfc1034](https://tools.ietf.org/html/rfc1034) & [rfc1123](https://tools.ietf.org/html/rfc1123)
* [rfc5234](https://tools.ietf.org/html/rfc5234) ABNF Rules


## Is it fast?

It should be fast enough (i.e: not a bottleneck) for those using
libraries and frameworks written in pure Python. Also, it can just
be used in some of the input/output headers.

It should be quite fast in future PyPy3, though.


## License

MIT
