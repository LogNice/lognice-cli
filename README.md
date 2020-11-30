# Log(N)ice CLI 🚀🚀🚀

```
docker build -t lognice_cli .
docker run --rm lognice_cli [command] [options]
```

### Create a session

Create a `Validator` class like so:

```python
class Validator:
    def tests(self):
        return [
            {
                'input': {'n': i},
                'output': 2 * i
            }
            for i in range(100)
        ]

```

Then run:

```shell
docker run --rm lognice_cli create -f validator.py
```

### Submit a solution

Create a `Solution` class like so:

```python
class Solution:
    def solve(self, n):
        return 2 * n
```

Then run:

```shell
docker run --rm lognice_cli submit -s session_id -f solution.py -u username
```

### Get results

#### Table summary

```shell
docker run --rm lognice_cli summary -s session_id
```

Example output:

```
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

#### Graph summary

You can also download a bar plot image containing the results of a session.

```shell
docker run --rm lognice_cli graph -s session_id
```
