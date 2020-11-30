# Log(N)ice CLI 🚀🚀🚀

```
docker build -t lognice-cli .
docker run --rm lognice-cli [command] [options]
```

#### Create a session

```shell
$ cat validator.py
class Validator:
    def tests(self):
        return [{'input': {'n': i}, 'output': 2 * i} for i in range(100)]
$ docker run --rm lognice-cli create -f validator.py
Session id: 2dc85
```

#### Submit a solution

```shell
$ cat solution.py
class Solution:
    def solve(self, n):
        return 2 * n
$ docker run --rm lognice-cli submit -s 2dc85 -f solution.py -u fancy_username
...
```

#### Get results

##### Table summary

```shell
$ docker run --rm lognice-cli summary -s 2dc85
+-----------------------------------+
|          [2dc85] Ranking          |
+------+-----------+----------------+
| Rank |  Username | CPU Time in us |
+------+-----------+----------------+
|  1   | username1 |       76       |
|  2   | username2 |       77       |
|  3   | username3 |       78       |
+------+-----------+----------------+
```

##### Graph summary

```shell
$ docker run --rm lognice-cli graph -s 2dc85
Image saved in 2dc85.png
```
