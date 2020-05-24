## Discrete social recommendation 阅读报告

Discrete social recommendation(DSR) 基本就是 DCF 的基础上加上社会化推荐，具体来说就是user之间的关联。所以它的优化方法基本上和 DCF 是一样的。

* 出现的错误

  这篇论文出现了一些细节上的错误，在这里罗列一下：

  * Optimizing D：

    <img src="C:\Users\QJ\AppData\Roaming\Typora\typora-user-images\image-20200221223300454.png" alt="image-20200221223300454" style="zoom: 33%;" />

    应为：
    $$
    \hat{d}_{ik} = \sum_{j \in\{j|i\in v_{j}\}}R_{ji}b_{jk} - \sum_{j \in\{j|i\in v_{j}\}}\mathbf{b}_{j}^{T}\mathbf{d}_{i}b_{jk} + \sum_{j \in\{j|i\in v_{j}\}}d_{ik} + \beta_2y_{ik}
    $$

  * Optimizing F:

    <img src="C:\Users\QJ\AppData\Roaming\Typora\typora-user-images\image-20200221224114719.png" alt="image-20200221224114719" style="zoom:33%;" />

    应为：
    $$
    \hat{f}_{ik} = \alpha_{0}\left(\sum_{j \in\{j|i\in N_{j}\}}S_{ji}b_{jk} - \sum_{j \in\{j|i\in N_{j}\}}\mathbf{b}_{j}^{T}\mathbf{f}_{i}b_{jk} + \sum_{j \in\{j|i\in N_{j}\}}f_{ik}\right) + \beta_3z_{ik}
    $$
    

  * 由于 $\mathbf{b}_{i}^{T}\mathbf{d}_{j}$ 和 $\mathbf{b}_{i}^{T}\mathbf{f}_{j}$  的范围都为$[-r, r]$， 所以 $R$ 和 $S$ 应该要映射到相同的范围

* 初始化

  U：
  $$
  \mathbf{u}_{i} = \left(\sum_{j\in v_{i}}\mathbf{v}_{j}\mathbf{v}_{j}^{T} + \alpha\sum_{j\in v_{i}}\mathbf{t}_{j}\mathbf{t}_{j}^{T}+\beta_{1}\mathbf{I}\right)^{-1}\left(\sum_{j\in v_{i}}R_{ij}\mathbf{v}_{j}+\alpha\sum_{j\in v_{i}}S_{ij}\mathbf{t}_{j}+\beta_{1}\mathbf{x}_{i}\right)
  $$
  V:
  $$
  \mathbf{v}_{j}=\left(\sum_{i\in\{i|j\in v_{i}\}}\mathbf{u}_{i}\mathbf{u}_{i}^{T}+\beta_{2}\mathbf{I}\right)^{-1}\left(\sum_{i\in\{i|j\in v_{i}\}}R_{ij}\mathbf{u}_{i} + \beta_{2}\mathbf{y}_{j}\right)
  $$
  T:
  $$
  \mathbf{t}_{j}=\left(\alpha\sum_{i\in\{i|j\in N_{i}\}}\mathbf{u}_{i}\mathbf{u}_{i}^{T}+\alpha\beta_{3}\mathbf{I}\right)^{-1}\left(\alpha\sum_{i\in\{i|j\in N_{i}\}}S_{ij}\mathbf{u}_{i} + \beta_{3}\mathbf{z}_{j}\right)
  $$



* 实验结果

  * 损失函数

    <img src="C:\Users\QJ\AppData\Roaming\Typora\typora-user-images\image-20200222100905962.png" alt="image-20200222100905962" style="zoom:67%;" />

  * NDCG

    * 计算NDCG时遇到了一些问题

      假设一共有5个item，

      那么对于一个user，他在测试集里的评分是 [2.5, 0, 3, 0, 3.5] (0代表没有评过分)，

      模型预测的结果是 [2, 2.5, 0.5, 3, 1.5]

       

      那计算ndcg_score (y_true, y_score)时，以下哪种是正确的方法：

      * ndcg_score ([2.5, 0, 3, 0, 3.5], [2, 2.5, 0.5, 3, 1.5])
      * ndcg_score ([2.5, 3, 3.5], [2, 0.5, 1.5])
      * ndcg_score ([2.5, 0, 3, 0, 3.5], [2, 0, 0.5, 0, 1.5])

    * 以上三种方法得出的结果和论文都不太接近。但是参考DCF这篇论文得出的结果，大多数的情况下NDCG都比0.7大，其中很多都达到了0.8以上。而这篇 DSR 得到的结果几乎处于0.3-0.5，比DCF低很多。按道理DSR增加了了社会化推荐，结果应该更好（虽然两者使用的数据集不同）。如果以 DCF 为参考，上面的第二种算法比较符合：

      <img src="C:\Users\QJ\AppData\Roaming\Typora\typora-user-images\image-20200222101847999.png" alt="image-20200222101847999" style="zoom:67%;" />

      

    