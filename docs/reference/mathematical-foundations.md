# Mathematical Foundations

## 8.1 Spectral Indices

All indices computed from Sentinel-2 L2A surface reflectance bands.

### Sentinel-2 Band Reference

| Band ID | Centre Wavelength (nm) | Resolution (m) |
|---------|------------------------|----------------|
| B02 | 490 (Blue) | 10 |
| B03 | 560 (Green) | 10 |
| B04 | 665 (Red) | 10 |
| B08 | 842 (NIR broad) | 10 |
| B11 | 1610 (SWIR-1) | 20 |
| B12 | 2190 (SWIR-2) | 20 |

### NDVI

$$\text{NDVI} = \frac{\rho_{\text{NIR}} - \rho_{\text{Red}}}{\rho_{\text{NIR}} + \rho_{\text{Red}}} = \frac{B_{08} - B_{04}}{B_{08} + B_{04}}$$

Range: $[-1, +1]$. Urban green: $> 0.3$. Built-up: $< 0.1$.

### NDWI (McFeeters 1996)

$$\text{NDWI} = \frac{B_{03} - B_{08}}{B_{03} + B_{08}}$$

Open water: $> 0.0$.

### NDBI (Zha et al. 2003)

$$\text{NDBI} = \frac{B_{11} - B_{08}}{B_{11} + B_{08}}$$

Built-up: $> 0.0$.

### EVI (Huete et al. 2002)

$$\text{EVI} = 2.5 \cdot \frac{B_{08} - B_{04}}{B_{08} + 6 \cdot B_{04} - 7.5 \cdot B_{02} + 1}$$

### BSI (Rikimaru et al. 2002)

$$\text{BSI} = \frac{(B_{11} + B_{04}) - (B_{08} + B_{02})}{(B_{11} + B_{04}) + (B_{08} + B_{02})}$$

## 8.2 Retrieval Scoring

### Reciprocal Rank Fusion

$$\text{RRF}(d) = \sum_{R \in \{R_{\text{dense}}, R_{\text{sparse}}\}} \frac{1}{k + \text{rank}_R(d)}$$

$k = 60$ (default).

### Cross-Encoder Reranking

$$s_i = \text{CrossEncoder}(q, c_i)$$

## 8.3 Urban Resilience Composite Score

$$\text{URCS}(c) = \sum_{d \in D} w_d \cdot R_d(c)$$

$D = \{\text{physical}, \text{climate}, \text{social}, \text{infrastructure}\}$.

| Dimension | Weight $w_d$ |
|-----------|--------------|
| Physical | 0.30 |
| Climate | 0.30 |
| Social | 0.20 |
| Infrastructure | 0.20 |

## 8.4 Segregation Indices

### Dissimilarity Index

$$D = \frac{1}{2} \sum_{i=1}^{n} \left| \frac{g_i}{G} - \frac{m_i}{M} \right|$$

### Isolation Index

$$P^* = \sum_{i=1}^{n} \left[ \frac{g_i}{G} \cdot \frac{g_i}{t_i} \right]$$

## 8.5 Transit Accessibility

$$A(c) = \sum_{s \in S(c, r)} f(s) \cdot e^{-\lambda \cdot d(c, s)}$$

$r = 800$ m, $\lambda = 0.003$.

## 8.6 Land Consumption Rate (SDG 11.3.1)

$$\text{SDG}_{11.3.1} = \frac{\text{LCR}}{\text{PGR}}$$

$$\text{LCR} = \frac{\ln(U_{\text{land}}(t_1) / U_{\text{land}}(t_0))}{t_1 - t_0}$$

$$\text{PGR} = \frac{\ln(P(t_1) / P(t_0))}{t_1 - t_0}$$
