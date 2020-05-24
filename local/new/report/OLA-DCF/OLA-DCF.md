## OLA-DCF

### 全局符号

|  Notations   |                         Description                          |
| :----------: | :----------------------------------------------------------: |
| $\mathbf{R}$ |                        Rating matrix                         |
| $\mathbf{U}$ |                 User latent features matrix                  |
| $\mathbf{V}$ |                 Item latent features matrix                  |
|     $M$      |                     The number of users                      |
|     $N$      |                     The number of items                      |
|    $F(i)$    |                The set of user $i$’s friends                 |
|   $\phi_i$   |                  User $i$ 's social factor                   |
|     $d$      | $\mathbf{U} \in \mathbb{R}^{d×M}$, $\mathbf{V} \in \mathbb{R}^{d×N}$ |



### 模型推导

#### E-step:

这一部分的推导和结论暂且与OLA论文中的一样。（主要问题在于OLA在这一部分的推导中，用到了 $Lipschitz$ 连续性和 $Hoeffding$ 不等式。我不确定它们能不能直接应用于离散系统。）

#### M-step:

OLA的目标函数为：

<img src="C:\Users\QJ\AppData\Roaming\Typora\typora-user-images\image-20200321004858814.png" alt="image-20200321004858814" style="zoom:40%;" />

根据DCF的思路我们将其改成：
$$
\begin{align}

\mathop {argmin}_{\mathbf{\phi},\mathbf{U},\mathbf{V},\mathbf{X},\mathbf{Y},\mathbf{Z}} 
& \sum_{i,j\in \mathcal{V}}\left(R_{ij}-\phi_{i}^{T}V_{j}\right)^{2}
\\
+ &\delta_{\phi}\sum_{i=1}^{M}\left(\phi_{i}-\sum_{u\in F(i)_{k^*}}\alpha_{iu}^{*}U_{u}\right)^{T}\left(\phi_{i}-\sum_{u\in F(i)_{k^*}}\alpha_{iu}^{*}U_{u}\right)
\\
- &2\delta_{\phi}tr(\mathbf{U}^{T}\mathbf{\Phi}) -2\beta tr(\mathbf{\Phi}^{T}\mathbf{X})-2\gamma tr(\mathbf{U}^{T}\mathbf{Y})-2\eta tr(\mathbf{V}^T \mathbf{Z})
\\
\\
s.t.& \ \Phi\in \{±1\}^{d \times M},\Phi\in \{±1\}^{d \times M},\Phi\in \{±1\}^{d \times M},
\\
& \ \mathbf{X1}=\mathbf{0},\mathbf{Y1}=\mathbf{0},\mathbf{Z1}=\mathbf{0},
\\
& \ \mathbf{XX}^{T}=M\mathbf{I},\mathbf{YY}^{T}=M\mathbf{I},\mathbf{ZZ}^{T}=N\mathbf{I}

\end{align}
\tag{1}
\label{1}
$$
其中，$\mathcal{V}$为$\mathbf{R}$中评分的索引集合，$\mathbf{\Phi} = \{\phi_{1},\phi_{2},...,\phi_{M}\}$，并假设$R_{ij} \in [-d,d]$.

* $\mathbf{XYZ}$子问题

  由于对 $\mathbf{X}$(或$\mathbf{Y,Z}$) 进行更新时，将其它项视为常数，所以对 $\mathbf{X}$(或$\mathbf{Y,Z}$) 的更新与 DCF 中的一致。

* $\mathbf{\Phi}$子问题

  目标函数：
  $$
  \begin{align}
  \mathop {argmin}_{\mathbf{\Phi}} 
  &\sum_{i,j\in\mathcal{V}}\left(R_{ij}-\phi_{i}^{T}V_{j} \right)^{2}
  \\
  + &\delta_{\phi}\sum_{i=1}^{M}\left(\phi_{i}-\sum_{u\in F(i)_{k^*}}\alpha_{iu}^{*}U_{u}\right)^{T}\left(\phi_{i}-\sum_{u\in F(i)_{k^*}}\alpha_{iu}^{*}U_{u}\right)
  \\
  - &2\delta_{\phi}tr(\mathbf{U}^{T}\mathbf{\Phi}) -2\beta tr(\mathbf{\Phi}^{T}\mathbf{X})
  \end{align}
  \tag{2}
  \label{2}
  $$
  令
  $$
  \begin{align}
  &\mathbf{G}=\left\{\sum_{u\in F(1)_{k^*}}\alpha_{1u}^*U_{u},\sum_{u\in F(2)_{k^*}}\alpha_{2u}^*U_{u},...,\sum_{u\in F(M)_{k^*}}\alpha_{Mu}^*U_{u}\right\}
  \\
  \\
  &\mathbf{E} = \delta_{\phi}\mathbf{G}+\delta_{\phi}\mathbf{U}+\beta \mathbf{X}
  \end{align}
  $$
  $\eqref{2}$ 可化简为
  $$
  \begin{align}
  \mathop {argmin}_{\mathbf{\Phi}} 
  &\sum_{i,j\in\mathcal{V}}\left(R_{ij}-\phi_{i}^{T}V_{j} \right)^{2}
  - 2\delta_{\phi}tr(\mathbf{\Phi}^{T}\mathbf{G})- 2\delta_{\phi}tr(\mathbf{\Phi}^{T}\mathbf{U}) -2\beta tr(\mathbf{\Phi}^{T}\mathbf{X})
  \\
  =\mathop {argmin}_{\mathbf{\Phi}} 
  &\sum_{i,j\in\mathcal{V}}\left(R_{ij}-\phi_{i}^{T}V_{j} \right)^{2}
  - 2tr\left(\mathbf{\Phi}^{T}(\delta_{\phi}\mathbf{G}+\delta_{\phi}\mathbf{U}+\beta \mathbf{X})\right)
  \\=\mathop {argmin}_{\mathbf{\Phi}} 
  &\sum_{i,j\in\mathcal{V}}\left(R_{ij}-\phi_{i}^{T}V_{j} \right)^{2}
  - 2tr\left(\mathbf{\Phi}^{T}\mathbf{E}\right)
  \end{align}
  \tag{3}
  \label{3}
  $$
  考虑 $\phi_{i}$:
  $$
  \begin{align}
  &\mathop {argmin}_{\phi_{i}} \sum_{j\in\mathcal{V}_{i}}\left(R_{ij}-\phi_{i}^{T}V_{j}\right)^{2} -2\phi_{i}^{T}E_{i}
  \\
  = &\mathop {argmin}_{\phi_{i}} \sum_{j\in\mathcal{V}_{i}}\left((\phi_{i}^{T}V_{j})^{2}-2R_{ij}\phi_{i}^{T}V_{j}\right) -2\phi_{i}^{T}E_{i}
  \\
  = &\mathop {argmin}_{\phi_{i}} \sum_{j\in\mathcal{V}_{i}}(\phi_{i}^{T}V_{j})^{2}-2(\sum_{j\in\mathcal{V}_{i}}R_{ij}V_{j}^{})\phi_{i}^{T} -2\phi_{i}^{T}E_{i}
  \end{align}
  \tag{4}
  \label{4}
  $$
  其中 $\mathcal{V}_{i} = \{j|(i,j)\in \mathcal{V}\}$ .

  考虑 $\phi_{ik}$:
  $$
  \mathop {argmin}_{\phi_{ik}\in±1} \sum_{j\in\mathcal{V}_{i}}(\phi_{i}^{T}V_{j})^{2}-2(\sum_{j\in\mathcal{V}_{i}}R_{ij}V_{j}^{T})\phi_{i}^{T} -2\phi_{i}^{T}E_{i}
  \tag{5}
  \label{5}
  $$
  其中
  $$
  \begin{align}
  \sum_{j\in\mathcal{V}_{i}}\left(\phi_{i}^{T}V_{j}\right)^{2}= &2\phi_{ik}(\sum_{j\in\mathcal{V}_{i}}V_{jk}\phi_{i\overline{k}}^{T}V_{j\overline{k}})
  \\
  + &\underbrace{\sum_{j\in\mathcal{V}_{i}}\left((\phi_{ik}V_{jk})^{2} +(\phi_{i\overline{k}}^{T}V_{j\overline{k}})^{2}\right) }_{constant}
  \\
  -2(\sum_{j\in\mathcal{V}_{i}}R_{ij}V_{j}^{T})\phi_{i}^{T} -2\phi_{i}^{T}E_{i} =&-2\phi_{ik}\sum_{j\in\mathcal{V}_{i}}R_{ij}V_{jk}-2\phi_{ik}E_{ik}
  \\
  &
  \underbrace{
  -2(\sum_{j\in\mathcal{V}_{i}}R_{ij}V_{j\overline{k}}^{T})\phi_{i\overline{k}}-2\phi_{i\overline{k}}E_{i\overline{k}}
  }_{constant}
  \end{align}
  $$
  故$\eqref{5}$等价于：
  $$
  \mathop {argmin}_{\phi_{ij}\in±1} \phi_{ik}\hat{\phi}_{ik}
  \\
  \hat{\phi}_{ik} = \sum_{j\in \mathcal{V}_{i}}V_{jk}(\phi_{i\overline{k}}^{T}V_{j\overline{k}}-R_{ij})-E_{ik}
  \tag{6}
  \label{6}
  $$
  $\phi_{ik}$ 取与 $\hat{\phi}_{ik}$ 异号即可。

* $\mathbf{U}$ 子问题

  目标函数：
  $$
  \mathop {argmin}_{\mathbf{U}}\delta_{\phi} \sum_{i=1}^{M}\left(\phi_{i}-\sum_{u\in F(i)_{k^*}}\alpha_{iu}^{*}U_{u}\right)^{T}\left(\phi_{i}-\sum_{u\in F(i)_{k^*}}\alpha_{iu}^{*}U_{u}\right)
  -2\delta_{\phi}tr(\mathbf{U}^{T}\mathbf{\Phi})-2\gamma tr(\mathbf{U}^{T}\mathbf{Y})
  \tag{7}
  \label{7}
  $$
  设 $\mathbf{F} = \delta_{\phi}\mathbf{\Phi}+\gamma\mathbf{Y}$，则 $\eqref{7}$ 等价于：
  $$
  \begin{align}
  &\mathop {argmin}_{\mathbf{U}}\delta_{\phi} \sum_{i=1}^{M}\left(\phi_{i}-\sum_{u\in F(i)_{k^*}}\alpha_{iu}^{*}U_{u}\right)^{T}\left(\phi_{i}-\sum_{u\in F(i)_{k^*}}\alpha_{iu}^{*}U_{u}\right)
  -2tr\left(\mathbf{U}^{T}(\delta_{\phi}\mathbf{\Phi}+\gamma\mathbf{Y})\right)
  \\
  = \ &\mathop {argmin}_{\mathbf{U}}\delta_{\phi} \sum_{i=1}^{M}\left(\phi_{i}-\sum_{u\in F(i)_{k^*}}\alpha_{iu}^{*}U_{u}\right)^{T}\left(\phi_{i}-\sum_{u\in F(i)_{k^*}}\alpha_{iu}^{*}U_{u}\right)
  -2tr\left(\mathbf{U}^{T}\mathbf{F}\right)
  \end{align}
  \tag{8}
  \label{8}
  $$
  设 $E(u) = \{i|u\in F(i)_{k^*}\}$，考虑 $\mathbf{U}_{u}$:

  
  $$
  \mathop {argmin}_{\mathbf{U}_{u}} \delta_{\phi}\sum_{i\in E(u)}\left(\phi_{i}-\sum_{p\in F(i)_{k^*}}\alpha_{ip}^{*}U_{p}\right)^{T}\left(\phi_{i}-\sum_{p\in F(i)_{k^*}}\alpha_{ip}^{*}U_{p}\right)-2{U}_{u}^{T}{F}_{u}
  \tag{9}
  \label{9}
  $$
  其中
  $$
  \begin{align}
  & \mathop {argmin}_{} \ \left(\phi_{i}-\sum_{p\in F(i)_{k^*}}\alpha_{ip}^{*}U_{p}\right)^{T}\left(\phi_{i}-\sum_{p\in F(i)_{k^*}}\alpha_{ip}^{*}U_{p}\right)
  \\
  \\
  = \ & \mathop {argmin}_{} \  \phi_{i}^{T}\phi_{i}-2\phi_{i}^{T}\sum_{p\in F(i)_{k^*}}\alpha_{ip}^{*}U_{p}+\sum_{m,n\in F(i)_{k^*}}\alpha_{im}^{*}\alpha_{in}^{*}U_{m}^{T}U_{n}
  \\
  \\
  = \ & \mathop {argmin}_{} 
  
  \underbrace{
  \phi_{i}^{T}\phi_{i} }_{constant}
  
  -2\alpha_{iu}^{*}\phi_{i}^{T}U_{u}
  
  \underbrace{
  -2\phi_{i}^{T}\sum_{p\in F(i)_{k^*} \\ \land p \neq u}\alpha_{ip}^{*}U_{p}}_{constant}
  +\sum_{m,n\in F(i)_{k^*}}\alpha_{im}^{*}\alpha_{in}^{*}U_{m}^{T}U_{n}
  \\
  = \ & \mathop {argmin}_{} \ -2\alpha_{iu}^{*}\phi_{i}^{T}U_{u}+
  \underbrace{
  (\alpha_{iu}^{*})^{2}U_{u}^{T}U_{u}}_{constant}
  
  +2\sum_{p\in F(i)_{k^*} \\ \land p \neq u}\alpha_{ip}^{*}\alpha_{iu}^{*} U_{p}^{T} U_{u}
  \\
  = \ & \mathop {argmin}_{} \ -\alpha_{iu}^{*}\phi_{i}^{T}U_{u}
  
  +\sum_{p\in F(i)_{k^*} \\ \land p \neq u}\alpha_{ip}^{*}\alpha_{iu}^{*} U_{p}^{T} U_{u}
  
  \end{align}
  $$
  故 $\eqref{9}$ 等价于：
  $$
  \begin{align}
  & \mathop {argmin}_{\mathbf{U}_{u}} \ \delta_{\phi}\sum_{i\in E(u)}
  \left(-\alpha_{iu}^{*}\phi_{i}^{T}U_{u}
  
  +\sum_{p\in F(i)_{k^*} \\ \land p \neq u}\alpha_{ip}^{*}\alpha_{iu}^{*} U_{p}^{T} U_{u}\right)
  -{U}_{u}^{T}{F}_{u}
  \\
  = \ & \mathop{argmin}_{U_u} \  \delta_{\phi}U_{u}^{T}\sum_{i \in E(u)}\alpha_{iu}^{*}\left(-\phi_{i} + \sum_{p\in F(i)_{k^*} \\ \land p \neq u}\alpha_{ip}^{*}U_{p}\right)-U_{u}^{T}F_{u}
  \\
  = \ & \mathop{argmin}_{U_u} \  U_{u}^{T}\left(\delta_{\phi}\sum_{i \in E(u)}\alpha_{iu}^{*}\left(-\phi_{i} + \sum_{p\in F(i)_{k^*} \\ \land p \neq u}\alpha_{ip}^{*}U_{p}\right)-F_{u}\right)
  \\
  = \ & \mathop{argmin}_{U_u} \  U_{u}^{T} \hat{U}_{u}
  
  \end{align}
  \tag{10}
  \label{10}
  $$
  考虑 $U_{uk}$:
  $$
  \begin{align}
  & \mathop {argmin}_{U_{uk}} \ U_{uk}\hat{U}_{uk} 
  \underbrace{
  + U_{u\overline{k}}^{T}\hat{U}_{u\overline{k}}}_{constant}
  \\
  = \ & \mathop {argmin}_{U_{uk}} \ U_{uk}\hat{U}_{uk} 
  \\
  \hat{U}_{uk} &=  \delta_{\phi}\sum_{i \in E(u)}\alpha_{iu}^{*}\left(-\phi_{ik} + \sum_{p\in F(i)_{k^*} \\ \land p \neq u}\alpha_{ip}^{*}U_{pk}\right)-F_{uk}
  \end{align}
  \tag{11}
  \label{11}
  $$
  $U_{uk}$ 取与 $\hat{U}_{uk}$ 异号。

* $\mathbf{V}$ 子问题

  目标函数：
  $$
  \begin{align}
  &\mathop {argmin}_{\mathbf{V}} \sum_{i,j\in\mathcal{V}}\left(R_{ij}-\phi_{i}^{T}V_{j}\right)^{2} -2\eta tr(\mathbf{V}^{T}\mathbf{Z})
  \\
  \end{align}
  \tag{12}
  \label{12}
  $$
  这与 DCF 的 $\mathbf{B}$ 子问题是完全一样的，最后得出的$\hat{V}_{j}$为：
  $$
  \hat{V}_{jk} = \sum_{i\in \mathcal{V}_{j}}\phi_{ik}(\phi_{i\overline{k}}^{T}V_{j\overline{k}}-R_{ij})-\eta Z_{ik}
  \tag{13}
  \label{13}
  $$
  其中 $\mathcal{V}_{j} = \{i|(i,j)\in \mathcal{V}\}$ .

### 遗留问题

* 在 E-step 中， $Lipschitz$ 连续性和 $Hoeffding$ 不等式能否直接用于离散系统
* 感觉计算复杂度比较大

