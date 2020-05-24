

## ***Discrete Personalized Ranking*** 阅读报告

这一篇论文提出的模型与 *DCF* 基本一致， 不同的地方在于使用了 AUC 作为目标函数进行优化。因此，本篇报告主要是对**四个子问题**以及**初始化**问题的推导。

* **objective function**
  $$
  {\underset {B, D, X, Y}{\operatorname {arg\,min} }}
  {\underset {(u,i,j) \in D_{S}}{\operatorname {\sum} }}
  \frac{1}{|U||I_{u}^{+}||I_{u}^{-}|}
  \bigg(2r - \mathbf{b}_{u}^{T}(\mathbf{d}_{i}-\mathbf{d}_{j})\bigg)^{2}
  \\
  - 2 \alpha \, tr(\mathbf{B}^{T}\mathbf{X}) - 2 \beta \, tr(\mathbf{D}^{T}\mathbf{Y})
  \\
  s.t. \ \mathbf{B} \in \{±1\}^{r×n},\mathbf{D} \in \{±1\}^{r×m}
  \\
  \mathbf{X1}_{n} = 0, \, \mathbf{Y1}_{m} = 0, \, \mathbf{XX}^{T}=n\mathbf{I}_{r}, \, \mathbf{YY}^{T}=m\mathbf{I}_{r}
  $$

* **B-subproblem**
  $$
  \begin{equation}
  {\underset {b_{uk} \in {±1}}{\operatorname {arg \, min}}}
  \ 
  {\underset {i,j\in I}{\operatorname \sum}} \, z_{u}^{+}z_{u}^{-}r_{ui}(1-r_{uj})\bigg(((\mathbf{d}_{i}-\mathbf{d}_{j})^{T}\mathbf{b}_{u})^{2} 
  \\
  -4r(\mathbf{d}_{i}-\mathbf{d}_{j})^{T}\mathbf{b}_{u} \bigg) - 2\alpha n \mathbf{x}_{u}^{T}\mathbf{b}_{u}
  
  \tag{1}
  \end{equation}
  $$
  
  其中
  $$
  \begin{align*}
  ((\mathbf{d}_{i}-\mathbf{d}_{j})^{T}\mathbf{b}_{u})^{2}  =& \ 
  
  \underbrace{
  ((\mathbf{d}_{i\overline{k}}-\mathbf{d}_{j\overline{k}})^{T}\mathbf{b}_{u\overline{k}})^{2}
  + (({d}_{ik}-{d}_{jk})^{}{b}_{uk})^{2}
  }_{\text{constant}}
  
  \\
  +& \ 2(\mathbf{d}_{i\overline{k}}-\mathbf{d}_{j\overline{k}})^{T}\mathbf{b}_{u\overline{k}}({d}_{ik}-{d}_{jk}){b}_{uk}
  \\
  \\
  \\
  (\mathbf{d}_{i}-\mathbf{d}_{j})^{T}\mathbf{b}_{u} =& \ 
    \underbrace{
    (\mathbf{d}_{i\overline{k}}-  \mathbf{d}_{j\overline{k}})^{T}\mathbf{b}_{u\overline{k}}
    }_{constant}
    +({d}_{ik}-{d}_{jk})^{}{b}_{uk}
  \\
  \\
  \\
  \mathbf{x}_{u}^{T}\mathbf{b}_{u} =&  \ \underbrace{\mathbf{x}_{u\overline{k}}^{T}\mathbf{b}_{u\overline{k}}}_{constant} +
  x_{uk}b_{uk}
  \end{align*}
  $$
  
  故式 (1) 等价于：
  $$
  \begin{align*}
  {\underset {b_{uk} \in {±1}}{\operatorname {arg \, min}}}
  \ 
  {\underset {i,j\in I}{\operatorname \sum}} \, z_{u}^{+}z_{u}^{-}r_{ui}(1-r_{uj})\bigg((\mathbf{d}_{i\overline{k}}-\mathbf{d}_{j\overline{k}})^{T}\mathbf{b}_{u\overline{k}}({d}_{ik}-{d}_{jk}){b}_{uk}
  \\
  -2r({d}_{ik}-{d}_{jk})^{}{b}_{uk} \bigg) - \alpha n x_{uk}b_{uk}
  
  
  
  \tag{2}
  \end{align*}
  $$
  令 
  $$
  \hat{b}_{uk} = {\underset {i,j\in I}{\operatorname \sum}} \, z_{u}^{+}z_{u}^{-}r_{ui}(1-r_{uj})\bigg((\mathbf{d}_{i\overline{k}}-\mathbf{d}_{j\overline{k}})^{T}\mathbf{b}_{u\overline{k}}({d}_{ik}-{d}_{jk})
  \\
  -2r({d}_{ik}-{d}_{jk}) \bigg) - \alpha n x_{uk}
  $$
  式 (2) 可以写成 
  $$
  {\underset {b_{uk} \in {±1}}{\operatorname {arg \, min}}} \ b_{uk}\hat{b}_{uk}
  $$



* **D-subproblem**

  与 **B-subproblem** 类似，不过似乎不能像 B-subproblem 一样并行计算。

* **X-subproblem**
  $$
  {\underset {\mathbf{X} \in {\mathbb{R}^{r ×n}}}{\operatorname {arg \, max}}} \ 
      tr(\mathbf{B}^{T}\mathbf{X}), \, s.t. \mathbf{X1} = 0, \, \mathbf{XX}^{T} = n\mathbf{I}
      \tag{3}
  $$
  论文给出了该问题的解为：
  $$
  \mathbf{X}^{*} = \sqrt{n}[\mathbf{P}_{b} \ \hat{\mathbf{P}}_{b}][\mathbf{Q}_{b} \ \hat{\mathbf{Q}}_{b}]^{T}
  \tag{4}
  $$

  * $[\mathbf{P}_{b} \  \hat{\mathbf{P}}_{b}]$  可以通过对 $\overline{\mathbf{B}}\overline{\mathbf{B}}^{T}$进行特征值分解得到
    $$
    \overline{\mathbf{B}}\overline{\mathbf{B}}^{T} =[\mathbf{P}_{b} \  \hat{\mathbf{P}}_{b}] \,
    \left[
     \begin{matrix}
       \mathbf{Σ}^2_b & \mathbf{0} \\
       \mathbf{0} & \mathbf{0}  
      \end{matrix} 
    \right] \,
    [\mathbf{P}_{b} \  \hat{\mathbf{P}}_{b}]^T
    $$
    其中：
    $$
    \overline{\mathbf{B}} = \mathbf{BJ}, \, \mathbf{J} = \mathbf{I} - \frac{1}{n}\mathbf{11}^T
    $$

  * $\mathbf{Q}_b \in \mathbb{R}^{m×r'}$ 可以通过 SVD 的定义得到
    $$
    \overline{\mathbf{B}} = \mathbf{P}_{b}\mathbf{Σ}_{b}\mathbf{Q}_{b}^{T} = \sum_{k=1}^{r'}\sigma_k\mathbf{p}_{k}\mathbf{q}_{k}^{T} \text{，其中$r'<r$是 $\overline{\mathbf{B}}$的秩，$\sigma_k$为奇异值 }\\
    \mathbf{Q}_{b} = \overline{\mathbf{B}}^{T}\mathbf{P}_{b}\mathbf{Σ}^{-1}_{b}
    $$

  * $\hat{\mathbf{Q}}_{b}$ 可以通过对 $[\mathbf{Q}_b \ \mathbf{1}]$ 进行 Gram-Schmidt 正交化得到

    

  下面证明 (4) 是 (3) 的最优解：

  * 先证明 (4) 是可行解，即 $\mathbf{X}^{*}\in\mathcal{B} =\{\mathbf{X}\in \mathbb{R}^{r×n}|\mathbf{X}\mathbf{1} = \mathbf{0},\mathbf{X}\mathbf{X}^{T} = n\mathbf{I}\}$.

    注意到 $\mathbf{J1} = \mathbf{0}$, 因此 $\mathbf{BJ1 = 0}$。因为 $\mathbf{BJ}$ 与 $\mathbf{Q}_{b}^{T}$ 有相同的行空间，所以$\mathbf{Q}_{b}^{T}\mathbf{1} = \mathbf{0}$

    。并且，$\hat{\mathbf{Q}}_{b}$ 是通过对 $[\mathbf{Q}_b \ \mathbf{1}]$ 进行 Gram-Schmidt 正交化得到的，因此$\mathbf{\hat{Q}}_{b}^{T}\mathbf{1} = \mathbf{0}$。所以我们得到了$[\mathbf{Q}_{b} \ \hat{\mathbf{Q}}_{b}]^{T}\mathbf{1} = \mathbf{0}$, 即 $\mathbf{X^{*}1} = \mathbf{0}$。

    

    另一方面，$\mathbf{X}^{*}\mathbf{X}^{*T} =n[\mathbf{P}_{b} \ \hat{\mathbf{P}}_{b}][\mathbf{Q}_{b} \ \hat{\mathbf{Q}}_{b}]^{T}[\mathbf{Q}_{b} \ \hat{\mathbf{Q}}_{b}][\mathbf{P}_{b} \ \hat{\mathbf{P}}_{b}]^{T} = n\mathbf{I}_{r}$

    

  * 下面证明 (4) 是 (3) 的最优解：

    考虑任意 $\mathbf{X} \in \mathcal{B}$，由于$\mathbf{X}\mathbf{1} = \mathbf{0}$，所以$\mathbf{XJ} = \mathbf{XI} - \frac{1}{n}\mathbf{X11}^{T} = \mathbf{X}$，且$\left< \mathbf{B},\mathbf{X}\right> = \left< \mathbf{B},\mathbf{XJ}\right> = \left< \mathbf{BJ},\mathbf{X}\right>$。
    $$
    \begin{align}
    tr(\mathbf{B}^{T}\mathbf{X}^{*}) &=\left< \mathbf{B},\mathbf{X}^{*}\right> = \left< \mathbf{BJ},\mathbf{X}^{*}\right>\\
    &=\left<[\mathbf{P}_{b} \ \hat{\mathbf{P}}_{b}]
    \left[
     \begin{matrix}
       \mathbf{Σ}_b & \mathbf{0} \\
       \mathbf{0} & \mathbf{0}  
      \end{matrix} 
    \right] \,
    [\mathbf{Q}_{b} \ \hat{\mathbf{Q}}_{b}]^{T}, \mathbf{X}^{*}\right>\\
    &=\sqrt{n} \left<
    \left[
     \begin{matrix}
       \mathbf{Σ}_b & \mathbf{0} \\
       \mathbf{0} & \mathbf{0}  
      \end{matrix} 
    \right],\mathbf{I}_{n}
    \right> \\
    &= \sqrt{n}{\overset {r'}{{\underset {k=1}{\operatorname \sum}}}}
    \sigma_k
    
    \end{align}
    $$
    根据 *Neumann’s trace inequality* 以及 $\mathbf{XX}^{T} = n\mathbf{I}_{r}$有，
    $$
    \left<\mathbf{BJ},\mathbf{X}\right> \leq \sqrt{n}\sum_{k=1}^{r'}\sigma_k
    $$
    因此，对于任意$\mathbf{X} \in \mathcal{B}$：
    $$
    \begin{align}
    tr(\mathbf{B}^{T}\mathbf{X}) &= \left<\mathbf{B},\mathbf{X}\right> =\left<\mathbf{BJ},\mathbf{X}\right>\\
    &\leq \sqrt{n}{\overset {r'}{{\underset {k=1}{\operatorname \sum}}}}
    \sigma_k\\
    &=tr(\mathbf{B}^{T}\mathbf{X}^{*})
    \end{align}
    $$
    

* **Y-subproblem**

  与 **X-subproblem** 类似



* **初始化**

  * 目标函数
    $$
    {\underset {\mathbf{P,Q,X,Y}}{\operatorname {arg \, min}}} \  \sum_{u,i,j}z_{u}^{+}z_{u}^{-}r_{ui}(1-r_{uj})(1-\mathbf{p}_{u}^{T}(\mathbf{q}_{i}-\mathbf{q}_{j}))^{2} + \\\alpha_{1}n||\mathbf{P}||^{2}_{F}+\beta_{1}n||\mathbf{Q}||^{2}_{F}-2\alpha_{2}ntr(\mathbf{P}^{T}\mathbf{X})-2\beta_{2}ntr(\mathbf{Q}^{T\mathbf{Y}})\\
    s.t. \mathbf{X1}_n = 0, \mathbf{Y1}_{m} = 0, \mathbf{XX}^{T}=n\mathbf{I}_{r},\mathbf{YY}^{T}=m\mathbf{I}_{r}
    \tag{5}
    $$

  * $\mathbf{X}$ 和 $\mathbf{Y}$ 可以通过 **X/Y-subproblem** 的解进行更新

  * $\mathbf{P}$ 和 $\mathbf{Q}$ 基于令相应的偏导数为 0 更新，但是论文并没有给出公式。

  * 固定$\mathbf{Q、X、Y}$，更新$\mathbf{P}$

    考虑 $\mathbf{p}_{u}$：
    $$
    \begin{align}
    &\ {\underset {\mathbf{p}_{u}}{\operatorname {arg \, min}}} \  \sum_{i,j}z_{u}^{+}z_{u}^{-}r_{ui}(1-r_{uj})(1-\mathbf{p}_{u}^{T}(\mathbf{q}_{i}-\mathbf{q}_{j}))^{2} +
    \alpha_{1}n||\mathbf{p}_{u}||^{2}-2\alpha_{2}n\mathbf{p}_{u}^{T}\mathbf{x}_{u}
    \\
    =&\ {\underset {\mathbf{p}_{u}}{\operatorname {arg \, min}}} \  \sum_{i,j}z_{u}^{+}z_{u}^{-}r_{ui}(1-r_{uj})((\mathbf{p}_{u}^{T}(\mathbf{q}_{i}-\mathbf{q}_{j}))^{2}-2\mathbf{p}_{u}^{T}(\mathbf{q}_{i}-\mathbf{q}_{j})) +
    \\
    &\alpha_{1}n||\mathbf{p}_{u}||^{2}-2\alpha_{2}n\mathbf{p}_{u}^{T}\mathbf{x}_{u}
    \\
    \end{align}
    $$
    

    令 $\mathcal{J} = \sum_{i,j}z_{u}^{+}z_{u}^{-}r_{ui}(1-r_{uj})((\mathbf{p}_{u}^{T}(\mathbf{q}_{i}-\mathbf{q}_{j}))^{2}-2\mathbf{p}_{u}^{T}(\mathbf{q}_{i}-\mathbf{q}_{j})) +
    \alpha_{1}n||\mathbf{p}_{u}||^{2}-2\alpha_{2}n\mathbf{p}_{u}^{T}\mathbf{x}_{u}$
    $$
    \frac{\partial\mathcal{J}}{\partial\mathbf{p}_{u}}=\sum_{i,j}z_{u}^{+}z_{u}^{-}r_{ui}(1-r_{uj})(2\mathbf{p}_{u}^{T}(\mathbf{q}_{i}-\mathbf{q}_{j})(\mathbf{q}_{i}-\mathbf{q}_{j})-2(\mathbf{q}_{i}-\mathbf{q}_{j})) + 2\alpha_{1}n\mathbf{p}_{u}-2\alpha_{2}n\mathbf{x}_{u} = 0
    $$
    化简得：
    $$
    \begin{align}
    &\sum_{i,j}z_{u}^{+}z_{u}^{-}r_{ui}(1-r_{uj})\mathbf{p}_{u}^{T}(\mathbf{q}_{i}-\mathbf{q}_{j})(\mathbf{q}_{i}-\mathbf{q}_{j}) + \alpha_{1}n\mathbf{p}_{u} = \sum_{i,j}z_{u}^{+}z_{u}^{-}r_{ui}(1-r_{uj})(\mathbf{q}_{i}-\mathbf{q}_{j})+\alpha_{2}n\mathbf{x}_{u}
    \\
    &\sum_{i,j}z_{u}^{+}z_{u}^{-}r_{ui}(1-r_{uj})(\mathbf{q}_{i}-\mathbf{q}_{j})^{T}(\mathbf{q}_{i}-\mathbf{q}_{j})\mathbf{p}_{u} + \alpha_{1}n\mathbf{I}_{r}\mathbf{p}_{u} = \sum_{i,j}z_{u}^{+}z_{u}^{-}r_{ui}(1-r_{uj})(\mathbf{q}_{i}-\mathbf{q}_{j})+\alpha_{2}n\mathbf{x}_{u}
    \\
    &\mathbf{p}_{u}^{*}=\left({\sum_{i,j}z_{u}^{+}z_{u}^{-}r_{ui}(1-r_{uj})(\mathbf{q}_{i}-\mathbf{q}_{j})^{T}(\mathbf{q}_{i}-\mathbf{q}_{j}) + \alpha_{1}n\mathbf{I}_{r}}\right)^{-1}\left(\sum_{i,j}z_{u}^{+}z_{u}^{-}r_{ui}(1-r_{uj})(\mathbf{q}_{i}-\mathbf{q}_{j})+\alpha_{2}n\mathbf{x}_{u}\right)
    \end{align}
    $$

  * 固定$\mathbf{P、X、Y}$，更新$\mathbf{Q}$

    考虑 $\mathbf{q}_{i}$：
    $$
    \begin{align}
    &\ {\underset {\mathbf{q}_{i}}{\operatorname {arg \, min}}}\sum_{u,j}z_{u}^{+}z_{u}^{-}r_{ui}(1-r_{uj})(1-\mathbf{p}_{u}^{T}(\mathbf{q}_{i}-\mathbf{q}_{j}))^{2} 
    \\
    &+ \sum_{u,j}z_{u}^{+}z_{u}^{-}r_{uj}(1-r_{ui})(1-\mathbf{p}_{u}^{T}(\mathbf{q}_{j}-\mathbf{q}_{i}))^{2} 
    \\
    &+\beta_{1}n||\mathbf{q}_{i}||^{2}-2\beta_{2}n\mathbf{q}_{i}^{T}\mathbf{y}_{i}
    \\
    =& \ {\underset {\mathbf{q}_{i}}{\operatorname {arg \, min}}}\sum_{u,j}z_{u}^{+}z_{u}^{-}r_{ui}(1-r_{uj})((\mathbf{p}_{u}^{T}(\mathbf{q}_{i}-\mathbf{q}_{j}))^{2}-2\mathbf{p}_{u}^{T}(\mathbf{q}_{i}-\mathbf{q}_{j}))
    \\
    &+ \sum_{u,j}z_{u}^{+}z_{u}^{-}r_{uj}(1-r_{ui})((\mathbf{p}_{u}^{T}(\mathbf{q}_{j}-\mathbf{q}_{i}))^{2}-2\mathbf{p}_{u}^{T}(\mathbf{q}_{j}-\mathbf{q}_{i}))
    \\
    &+ \beta_{1}n||\mathbf{q}_{i}||^{2}-2\beta_{2}n\mathbf{q}_{i}^{T}\mathbf{y}_{i}
    \\
    
    \end{align}
    $$
    令
    $$
    \begin{align}
    \mathcal{L} =& \ {\underset {\mathbf{q}_{i}}{\operatorname {arg \, min}}}\sum_{u,j}z_{u}^{+}z_{u}^{-}r_{ui}(1-r_{uj})((\mathbf{p}_{u}^{T}(\mathbf{q}_{i}-\mathbf{q}_{j}))^{2}-2\mathbf{p}_{u}^{T}(\mathbf{q}_{i}-\mathbf{q}_{j}))
    \\
    &+ \sum_{u,j}z_{u}^{+}z_{u}^{-}r_{uj}(1-r_{ui})((\mathbf{p}_{u}^{T}(\mathbf{q}_{j}-\mathbf{q}_{i}))^{2}-2\mathbf{p}_{u}^{T}(\mathbf{q}_{j}-\mathbf{q}_{i}))
    \\
    &+ \beta_{1}n||\mathbf{q}_{i}||^{2}-2\beta_{2}n\mathbf{q}_{i}^{T}\mathbf{y}_{i}
    \\
    \end{align}
    $$

    
    $$
    \begin{align}
    \frac{\partial \mathcal{L}}{\partial \mathbf{q}_{i}} =& \sum_{u,j}z_{u}^{+}z_{u}^{-}r_{ui}(1-r_{uj})(2\mathbf{p}_{u}^{T}(\mathbf{q}_{i}-\mathbf{q}_{j})\mathbf{p}_{u}-2\mathbf{p}_{u})
    \\
    +& \sum_{u,j}z_{u}^{+}z_{u}^{-}r_{uj}(1-r_{ui})(2\mathbf{p}_{u}^{T}(\mathbf{q}_{j}-\mathbf{q}_{i})(-\mathbf{p}_{u})+2\mathbf{p}_{u})
    \\
    +& 2\beta_{1}n\mathbf{q}_{i}-2\beta_{2}n\mathbf{y}_{i}
    \\
    =&0
    \end{align}
    $$
    化简得：
    $$
    \begin{align}
    &\sum_{u,j}z_{u}^{+}z_{u}^{-}r_{ui}(1-r_{uj})(\mathbf{p}_{u}^{T}\mathbf{q}_{i}\mathbf{p}_{u})+\sum_{u,j}z_{u}^{+}z_{u}^{-}r_{uj}(1-r_{ui})(-\mathbf{p}_{u}^{T}\mathbf{q}_{i}\mathbf{p}_{u})
    +\beta_{1}n\mathbf{q}_{i}
    \\
    =& \sum_{u,j}z_{u}^{+}z_{u}^{-}r_{ui}(1-r_{uj})(1+\mathbf{p}_{u}^{T}\mathbf{q}_{j})\mathbf{p}_{u}+\sum_{u,j}z_{u}^{+}z_{u}^{-}r_{uj}(1-r_{ui})(\mathbf{p}_{u}^{T}\mathbf{q}_{i}-1)\mathbf{p}_{u}+\beta_{2}n\mathbf{y}_{i}
    \end{align}
    $$
    
    $$
    \begin{align}
    &\sum_{u,j}z_{u}^{+}z_{u}^{-}r_{ui}(1-r_{uj})(\mathbf{p}_{u}\mathbf{p}_{u}^{T})\mathbf{q}_{i}+\sum_{u,j}z_{u}^{+}z_{u}^{-}r_{uj}(1-r_{ui})(-\mathbf{p}_{u}\mathbf{p}_{u}^{T})\mathbf{q}_{i}
    +\beta_{1}n\mathbf{I}_{r}\mathbf{q}_{i}
    \\
    =& \sum_{u,j}z_{u}^{+}z_{u}^{-}r_{ui}(1-r_{uj})(1+\mathbf{p}_{u}^{T}\mathbf{q}_{j})\mathbf{p}_{u}+\sum_{u,j}z_{u}^{+}z_{u}^{-}r_{uj}(1-r_{ui})(\mathbf{p}_{u}^{T}\mathbf{q}_{i}-1)\mathbf{p}_{u}+\beta_{2}n\mathbf{y}_{i}
    \end{align}
    $$
    
    $$
    \begin{align}
    \mathbf{q}_{i}^{*} = &\left( \sum_{u,j}z_{u}^{+}z_{u}^{-}r_{ui}(1-r_{uj})(\mathbf{p}_{u}\mathbf{p}_{u}^{T})+\sum_{u,j}z_{u}^{+}z_{u}^{-}r_{uj}(1-r_{ui})(-\mathbf{p}_{u}\mathbf{p}_{u}^{T})
    +\beta_{1}n\mathbf{I}_{r}\right)^{-1}
    \\
    &\left(\sum_{u,j}z_{u}^{+}z_{u}^{-}r_{ui}(1-r_{uj})(1+\mathbf{p}_{u}^{T}\mathbf{q}_{j})\mathbf{p}_{u}+\sum_{u,j}z_{u}^{+}z_{u}^{-}r_{uj}(1-r_{ui})(\mathbf{p}_{u}^{T}\mathbf{q}_{i}-1)\mathbf{p}_{u}+\beta_{2}n\mathbf{y}_{i}\right)
    \end{align}
    $$
    



* 运行结果

  ![图片](C:\Users\QJ\Desktop\report\图片.png)