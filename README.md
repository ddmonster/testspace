
# config

## 自动生成迁移文件

使用alembic revision --autogenerate -m "message"将当前模型中的状态生成迁移文件。

## 更新数据库

使用alembic upgrade head将刚刚生成的迁移文件，真正映射到数据库中。同理，如果要降级，那么使用alembic downgrade head。

## 设置开发环境

  创建python venv 环境
  激活venv 安装requierments.txt中的依赖包
  设置src/testspace/data/config.toml中SQLALCHEMY_DATABASE_URL 的地址为postgresql 的连接
  example:
    postgresql://[username]:[passwrd]@[database url]:[port]/[db name]

## sqlalchemy

synchronize_session = "fetch"
 <https://docs.sqlalchemy.org/en/14/orm/session_basics.html#orm-expression-update-delete>

 Selecting a Synchronization Strategy
With both the 1.x and 2.0 form of ORM-enabled updates and deletes, the following values for synchronize_session are supported:

* False - don’t synchronize the session. This option is the most efficient and is reliable once the session is expired, which typically occurs after a commit(), or explicitly using expire_all(). Before the expiration, objects that were updated or deleted in the database may still remain in the session with stale values, which can lead to confusing results.

* 'fetch' - Retrieves the primary key identity of affected rows by either performing a SELECT before the UPDATE or DELETE, or by using RETURNING if the database supports it, so that in-memory objects which are affected by the operation can be refreshed with new values (updates) or expunged from the Session (deletes). Note that this synchronization strategy is not available if the given update() or delete() construct specifies columns for UpdateBase.returning() explicitly.

* 'evaluate' - Evaluate the WHERE criteria given in the UPDATE or DELETE statement in Python, to locate matching objects within the Session. This approach does not add any round trips and in the absence of RETURNING support is more efficient. For UPDATE or DELETE statements with complex criteria, the 'evaluate' strategy may not be able to evaluate the expression in Python and will raise an error. If this occurs, use the 'fetch' strategy for the operation instead.

## Generating distribution archives

<https://packaging.python.org/en/latest/tutorials/packaging-projects/>
The next step is to generate distribution packages for the package. These are archives that are uploaded to the Python Package Index and can be installed by pip.

Make sure you have the latest version of PyPA’s build installed:

Unix/macOS
python3 -m pip install --upgrade build

Windows
Tip If you have trouble installing these, see the Installing Packages tutorial.
Now run this command from the same directory where pyproject.toml is located:

Unix/macOS
python3 -m build

Windows
This command should output a lot of text and once completed should generate two files in the dist directory:

dist/
  example-package-YOUR-USERNAME-HERE-0.0.1-py3-none-any.whl
  example-package-YOUR-USERNAME-HERE-0.0.1.tar.gz
The tar.gz file is a source archive whereas the .whl file is a built distribution. Newer pip versions preferentially install built distributions, but will fall back to source archives if needed. You should always upload a source archive and provide built archives for the platforms your project is compatible with. In this case, our example package is compatible with Python on any platform so only one built distribution is needed.
