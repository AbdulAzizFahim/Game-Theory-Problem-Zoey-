from landsites import Land
from data_structures import bst
import random

class Mode1Navigator:
    """
    In the first Task we used Binary Search Tree to store ratio of each land's gold
    divided by guardians. We used the ratio as key as it is unique for all lands and
    used BST so that we can optimize time on query. We also used In order traversal
    to get the array sorted and reverse it so that we have the items from bigger to
    smaller.
    """

    def __init__(self, sites: list[Land], adventurers: int) -> None:
        """
        Idea: Store the gold/guarian ratio as key in BST. After inserting all the keys
        take the in order traversal and reverse to get the best land to worst land.

        Total Complexity = O(N*D + N + N) Where N is the nubmer of sites and D is
        the depth of BST.

        Best-case time complexity: O(N) - Because a balancing tree will balancing depth.
        Worst-case time complexity: O(N^2) - Because a skewed tree will have depth = N.
        """
        self.adventurers = adventurers
        self.bst = bst.BinarySearchTree()

        for land in sites:
            if land.get_guardians() == 0:
                ratio = 0
            else:
                ratio = land.get_gold()/land.get_guardians()
            self.bst.__setitem__(ratio,land)

        self.data = [node.item for node in bst.BSTInOrderIterator(self.bst.root)]
        self.data.reverse()

    def select_sites(self) -> list[tuple[Land, int]]:
        """
        Idea: If the number of adventurers is greater or equal to the guardian then consume the whole
        land with adventurers. Otherwise only send the current adventuers.

        Total Complexity = O(N) Where N is the number of lands.

        Best-case time complexity: O(1) - If there is no fighters/adventurers.
        
        Worst-case time complexity: O(N) - If there is enough fighters/adventurers we have to
        iterate the whole loop.
        """

        current = self.adventurers
        result = []
        for land in self.data:
            if current == 0:
                break
            if(current >= land.get_guardians()):
                current = current - land.get_guardians()
                result.append((land, land.get_guardians()))
            else:
                 result.append((land, current))
                 break
        return result
            


    def select_sites_from_adventure_numbers(self, adventure_numbers: list[int]) -> list[float]:
        """
        Idea: If the number of adventurers is greater or equal to the guardian then consume the whole
        land with adventurers. Otherwise only send the current adventuers. As the lands are sorted
        from best to worst we can use the previous result for the next one.This is something like a
        prefix sum to get us the desired value without using additonal loops. The last loop is for 
        remaining fighters who won't have any lands if applicable.

        Total Time Complexity = N + N(LogN) + N + N + L - Where N is the number of 
        adventure_numbers and L is the numberr of lands.

        Best-case time complexity: O(N(LogN)+ 3N) = O(N(LogN)) - If there is no fighters/adventurers and lands.
        
        Worst-case time complexity: O(N(LogN)+ 3N + L) = O(N(LogN)) - If there is enough fighters and land to interate
        the whole list.
        """

        attackers= sorted([[value, index] for index, value in enumerate(adventure_numbers)])
        land = self.data
        attackerIndex = 0
        result = [[0, tup[1]] for tup in attackers]
        landIndex = 0
        while(attackerIndex < len(attackers) and landIndex < len(land)):
            currentAttackers = attackers[attackerIndex][0]
            if attackerIndex != 0:
                currentAttackers -= attackers[attackerIndex-1][0]
                result[attackerIndex][0] += result[attackerIndex-1][0]
            if currentAttackers == 0:
                attackerIndex+=1
                continue 
            else:
                while(attackerIndex < len(attackers)):
                    if(landIndex >= len(land)):
                        break
                    if currentAttackers >= land[landIndex].get_guardians():
                        result[attackerIndex][0] += land[landIndex].get_gold()
                        currentAttackers -= land[landIndex].get_guardians()
                        landIndex+=1
                    else:
                        gold = min(((currentAttackers * land[landIndex].get_gold())/land[landIndex].get_guardians()),land[landIndex].get_gold())
                        result[attackerIndex][0] += gold
                        land[landIndex].set_guardians(land[landIndex].get_guardians() - currentAttackers)
                        currentAttackers = 0
                        land[landIndex].set_gold(land[landIndex].get_gold() - gold)
                        attackerIndex+=1
                        break

        while(attackerIndex < len(attackers)):
            if attackerIndex == 0 and result[attackerIndex][0] != 0:
                result[attackerIndex][0] += result[attackerIndex-1][0]
            attackerIndex+=1

        sorted_result = sorted(result, key=lambda x: x[1])         
        return [tup[0] for tup in sorted_result]          

    def update_site(self, land: Land, new_reward: float, new_guardians: int) -> None:
        """
        Idea: Delete the land from the BST with ratio. Insert the new land and update the in order interation
        and use reverse to get the best to worst lands.

        Total Time Complexity = O(D + D + D + D) = O(D) - Where D is the depth of the BST.
        Best-case time complexity: O(D+N) - Where D is the depth of the tree and N is the total element.
        We can also say O(N+Log(N)) because in balancing BST the depth is the Log of total length.
        
        Worst-case time complexity: O(N+D) - Where N is numbere of elements and D is the depth. We can
        also say O(N+D) because in skewed trees Depth = number of elements.
        """

        ratio = land.get_gold()/land.get_guardians()
        self.bst.__delitem__(ratio)

        new_ratio = new_reward/new_guardians
        self.bst.__setitem__(new_ratio,Land(land.name,new_reward,new_guardians))

        self.data = []
        self.data = [node.item for node in bst.BSTInOrderIterator(self.bst.root)]
        self.data.reverse()
