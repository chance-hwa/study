'''
문제
세포 내에서 유전자들은 특정 조절 네트워크를 통해 서로 영향을 미칠 수 있습니다. 일부 유전자는 다른 유전자의 발현을 촉진하거나 억제할 수 있습니다.

예를 들어, 유전자 A가 유전자 B를 조절하고, 유전자 B가 유전자 C를 조절하지만, 유전자 C는 유전자 A를 직접 조절하지 않을 수도 있습니다.

각 유전자 간의 조절 관계가 주어졌을 때, 독립적인 유전자 조절 그룹의 개수를 찾으세요.

입력:

regulation_network (2D list, n x n): 유전자 조절 관계를 나타내는 데이터.

regulation_network[i][j] = 1이면 유전자 i가 유전자 j의 발현을 조절함.

regulation_network[i][j] = 0이면 유전자 i가 유전자 j를 조절하지 않음.

항상 regulation_network[i][i] = 1 (유전자는 자기 자신을 조절 가능).

출력:

(int): 독립적인 유전자 조절 그룹(Clusters)의 개수.

'''
from collections import defaultdict

def find_gene_groups(regulation_network):
    gene2regulators = defaultdict(set)
    for i in range(len(regulation_network)):
        for j in range(len(regulation_network)):
            if regulation_network[i][j] == 1:
                gene2regulators[i].add(j)
    
    clusters = list()
    for gene in gene2regulators:
        regulators = gene2regulators[gene]
        if not clusters:
            clusters.append(regulators)
        else:
            for cluster in clusters:
                if cluster & regulators:
                    cluster.update(regulators)
                    break
            else:
                clusters.append(regulators)
    
    return len(clusters)
        

#Example test cases
regulation_network = [
    [1,1,0],  
    [0,1,1],  
    [0,0,1]
]
print(find_gene_groups(regulation_network))

regulation_network = [
    [1,0,0],  
    [0,1,1],  
    [0,0,1]
]
print(find_gene_groups(regulation_network))


"""
예제 1:

Input:
regulation_network = [
    [1,1,0],  
    [0,1,1],  
    [0,0,1]
]

Output:
1
유전자 0은 유전자 1을 조절하고, 유전자1은 유전자 2를 조절하므로 크게 1 개의 그룹을 형성함

예제 2:

Input:
regulation_network = [
    [1,0,0],  
    [0,1,1],  
    [0,0,1]
]

Output:
2
유전자 0은 독립적으로 존재하고, 유전자 1은 유전자 2를 조절하는 그룹 1개가 존재하므로 크게 2개의 그룹을 형성함
"""

