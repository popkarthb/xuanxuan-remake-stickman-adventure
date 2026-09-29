# 萱萱小游戏：火柴人大冒险重制版

**Stickman Adventure Remake**

一个根据童年回忆重新制作的火柴人冒险小游戏。

这个项目尝试把记忆中的火柴人探索、平台跳跃、射击、近战、钥匙、开关和区域连接等玩法重新做出来，并在后续开发中逐步完善游戏内容和体验。

## 游戏截图

游戏截图将放在 `image/` 目录中，并展示在这里。

<!--
![Stickman Adventure Screenshot 1](image/screenshot-01.png)
![Stickman Adventure Screenshot 2](image/screenshot-02.png)
-->

## 当前版本

当前原型包含：

- 1 个中心大厅
- 6 个主要区域
- 2 个深层区域
- 平台跳跃与移动
- 枪械与近战攻击
- 敌人与敌方子弹
- 弹药拾取
- 钥匙与开关机制
- 房间与区域之间的连接

## 运行

```bash
python -m pip install -r requirements.txt
python main.py
```

## 操作

- `←` / `→` 或 `A` / `D`：移动
- `↑` / `W` / `Space`：跳跃
- `Z` / `J` / `Left Ctrl`：开枪；弹药耗尽后使用拳头
- `R`：重新开始
- `Esc`：退出

人物接触可用的门会进入对应区域。部分路线需要钥匙或开关才能解锁。

## 项目状态

当前项目处于早期重制与玩法验证阶段，后续会继续优化地图、角色、战斗、视觉效果和整体游戏体验。
