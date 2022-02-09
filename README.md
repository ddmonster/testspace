自动生成迁移文件：
使用alembic revision --autogenerate -m "message"将当前模型中的状态生成迁移文件。

更新数据库：
使用alembic upgrade head将刚刚生成的迁移文件，真正映射到数据库中。同理，如果要降级，那么使用alembic downgrade head。
