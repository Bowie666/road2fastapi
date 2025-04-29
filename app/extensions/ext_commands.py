import time

import typer
from rich.progress import track

"""
TODO 
- 1 问题 没有办法像flask一样, 使用上下文来链接数据库, 估计得自己手动写一个, 太麻烦了回头在研究
- 2 fastapi的设计就不适合用click工具 目前typer和click都得独立使用
"""
# Typer CLI 应用
cli = typer.Typer()


"""
python ext_commands.py hello pass
Hello, pass!
"""
@cli.command()
def hello(name: str):
    """打印 Hello 命令行输出"""
    typer.echo(f"Hello, {name}!")


# from ext_redis import RedisDep
# @cli.command()
# def tryDB(name: str, redis: RedisDep):
#     """设置键值对到 Redis"""
#     redis.set(name, 'pass')
#     return {"message": f"Key '{name}' set with value 'pass'"}

# @cli.command()
# def trygetDB(name: str, redis: RedisDep):
#     """从Redis拿值"""
#     value = redis.get(name)
#     if value is None:
#         return {"message": f"Key '{name}' not found"}
#     return {"key": name, "value": value}

@cli.command()
def delete():
    """进度条及删除"""
    delete = typer.confirm("Are you sure you want to delete it?")
    if not delete:
        print("Not deleting")
        raise typer.Abort()
    # print("Deleting it!")

    total = 0
    for value in track(range(100), description="Processing..."):
        # Fake processing time
        time.sleep(0.01)
        total += 1
    print(f"Processed {total} things.")

if __name__ == "__main__":
    cli()


"""
# 这是最简单的使用方式

def main():
    delete = typer.confirm("Are you sure you want to delete it?")
    if not delete:
        print("Not deleting")
        raise typer.Abort()
    # print("Deleting it!")

    total = 0
    for value in track(range(100), description="Processing..."):
        # Fake processing time
        time.sleep(0.01)
        total += 1
    print(f"Processed {total} things.")


if __name__ == "__main__":
    typer.run(main)
"""