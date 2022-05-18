自动生成迁移文件：
使用alembic revision --autogenerate -m "message"将当前模型中的状态生成迁移文件。

更新数据库：
使用alembic upgrade head将刚刚生成的迁移文件，真正映射到数据库中。同理，如果要降级，那么使用alembic downgrade head。


##Generating distribution archives
https://packaging.python.org/en/latest/tutorials/packaging-projects/
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
