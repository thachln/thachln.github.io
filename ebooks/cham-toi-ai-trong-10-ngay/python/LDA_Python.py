import pandas as pd
file_path = 'https://thachln.github.io/datasets/iris-data.csv'
df = pd.read_csv(file_path)
df.head()

X = df.iloc[:, 0:4].values
X

Y = df.iloc[:, 4].values
Y


# Encode categorical class labels
from sklearn.preprocessing import LabelEncoder
class_le = LabelEncoder()
Y_num = class_le.fit_transform(Y)
Y_num

group_0 = X[Y_num==0]
group_0

group_0.T

# Construct within-class covariant scatter matrix S_W
# Tính ma trận ovariant scatter bên trong mỗi nhóm
import numpy as np
s_w = np.zeros((4,4))
s_w
for i in range(3):
    s_w += np.cov(X[Y_num==i].T)

s_w

# Construct between-class scatter matrix s_b
N = np.bincount(Y_num) # number of samples for given class
vecs=[]
[vecs.append(np.mean(X[Y_num==i], axis=0)) for i in range(3)] # class means
vecs

mean_overall = np.mean(X, axis=0) # overall mean
mean_overall


s_b = np.zeros((4,4))
for i in range(3):
    s_b += N[i]*(((vecs[i]-mean_overall).reshape(4,1)).dot(((vecs[i]-mean_overall).reshape(1,4))))
    
s_b


# Calculate sorted eigenvalues and eigenvectors of inverse(s_w)dot(s_b)
eigen_vals, eigen_vecs = np.linalg.eig(np.linalg.inv(s_w).dot(s_b))
eigen_pairs = [(np.abs(eigen_vals[i]), eigen_vecs[:,i]) for i in range(len(eigen_vals))]
eigen_pairs = sorted(eigen_pairs,key=lambda k: k[0], reverse=True)
print('Eigenvalues in decreasing order:\n')
for eigen_val in eigen_pairs:
    print(eigen_val[0])
    
# Plot main LDA components
import matplotlib.pyplot as plt
tot = sum(eigen_vals.real)
discr = [(i / tot) for i in sorted(eigen_vals.real, reverse=True)]
cum_discr = np.cumsum(discr)
plt.bar(range(1, 5), discr, width=0.2,alpha=0.5, align='center',label='individual "discriminability"')
plt.step(range(1, 5), cum_discr, where='mid',label='cumulative "discriminability"')
plt.ylabel('"discriminability" ratio')
plt.xlabel('Linear Discriminants')
plt.ylim([-0.1, 1.1])
plt.legend(loc='best')
plt.show()


# Project original features onto the new feature space
W = np.hstack((eigen_pairs[0][1][:, ].reshape(4,1),eigen_pairs[1][1][:, ].reshape(4,1))).real
X_train_lda = X.dot(W)

# Plot transformed features in LDA subspace
data=pd.DataFrame(X_train_lda)
data['class']=Y_num
data.columns=["LD1","LD2","class"]
data.head()

markers = ['s', 'x','o']
import seaborn as sns
sns.lmplot(x="LD1", y="LD2", data=data, markers=markers,fit_reg=False, hue='class', legend=False)
plt.legend(loc='upper center')
plt.show()

# LDA implementation using scikit-learn
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
lda = LinearDiscriminantAnalysis(n_components=2)
X_train_lda = lda.fit_transform(X, Y_num)

data = pd.DataFrame(X_train_lda)
data['class'] = Y_num
data.columns=["LD1","LD2","class"]
data.head()

markers = ['s', 'x','o']
colors = ['r', 'b','g']
sns.lmplot(x="LD1", y="LD2", data=data, hue='class', markers=markers,fit_reg=False,legend=False)
plt.legend(loc='upper center')
plt.show()