import numpy as np
import matplotlib.pyplot as plt

# 创建 x 轴数据，从 1（ln(1) = 0，不能除以 0）到 10，总共 1000 个点
x = np.linspace(1.01, 10, 1000)
# 计算 x/ln(x) 的值
y = x / np.log(x)

# 绘制图像
plt.plot(x, y, label='y = x/ln(x)')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Plot of y = x/ln(x)')

# y2 = x/ np.log2(x)
# plt.plot(x, y2, label='y = x/log2(x)')
# plt.xlabel('x')
# plt.ylabel('y2')
# plt.title('Plot of y2 = x/log2(x)')

y3 = x/ np.log(x+1)
plt.plot(x, y3, label='y = x/ln(x+1)')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Plot of y = x/ln(x+1)')

y4 = x / np.log(x+0.75)
plt.plot(x, y4, label='y = x/ln(x+0.5)')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Plot of y = x/ln(x+1)')
# 添加图例
plt.legend()

# 显示图像
plt.show()
