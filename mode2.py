from landsites import Land
from data_structures import heap
from data_structures import hash_table

class Mode2Navigator:
    """
    In task -2 We used heap and hash tables. At first we deduct a formula
    which is if any land has gold/guardian ratio <= 2.5 it is suboptimal
    to send adventurers. After that if the ratio is more than 2.5 we used
    another fomula = gold - (2.5 * guardian) for each sites. The highest
    score of this will be our candiates. We used heap to insert tuple of 
    (score, land_name) as it is unique in land name and used hash table to 
    store key = land name and value = land object. Hash tables is known 
    for fast insertion and deletion so it is an ideal data structure for us.
    """

    def __init__(self, n_teams: int) -> None:
        """
        Student-TODO: Best/Worst Case
        """
        self.myHeap = heap.MaxHeap(20)
        self.myTable = hash_table.LinearProbeTable[str,Land]()
        self.team_size = n_teams



    def add_sites(self, sites: list[Land]) -> None:
        """
        Idea: Ignore the lands which has gold/guardian ratio not more than 2.5
        After that from the highest land which has the best score formula.
        Score formula = gold - (2.5 * guardian)

        Total Time Complexity = O(NH) Where N is the number of sites
        and H is the height of heap. We can also say that O(NLog(N)) as 
        the height will be Log of number of elements.

        Best-case time complexity: O(NH/NLogN) - N = Number of site and H = height of heap.
        Worst-case time complexity: O(NH/NLogN) - N = Number of site and H = height of heap.
        """

        for land in sites:
            if land.get_guardians() == 0:
                ratio = 0
            else:
                ratio = land.get_gold()/land.get_guardians()
            if ratio > 2.5:
                self.myHeap.add((land.get_gold()-(2.5*land.get_guardians()),land.get_name()))
                self.myTable[land.get_name()] = land 

    def simulate_day(self, adventurer_size: int) -> list[tuple[Land | None, int]]:
        """
        Idea: The heap contains the best candidate land. Use it for the current team, update the
        gold and guardian and repeat the process until all of the teams are done with it.
        
        Total Complexity : O(K*(H+H)) - Where K is the number of total teams
        and H is the height of heap. As H = Log(N) we N is the number of sites
        we can also say that the total complexity is O(K*(LogN+LogN)) = O(K LogN)

        Best time complexity : O(K) where every land is suboptimal.
        Worst time complexity: O(KLogN) - where every land is optimal candiate.
        """

        result = []
        for index in range(0,self.team_size):
            if(self.myHeap.length == 0):
                result.append((None,0))
                continue

            current_max = self.myHeap.get_max()
            land = self.myTable[current_max[1]]
            total_send = min(land.get_guardians(),adventurer_size)
            result.append((land,total_send))
            gold_reduced = min((total_send*land.get_gold())/land.get_guardians(),land.get_gold())
            land.set_guardians(land.get_guardians() - total_send)
            land.set_gold(land.get_gold()-gold_reduced)



            if land.get_guardians() == 0:
                ratio = 0
            else:
                ratio = land.get_gold()/land.get_guardians()
            if ratio > 2.5:
                self.myHeap.add((land.get_gold()-(2.5*land.get_guardians()),land.get_name()))
                self.myTable[land.get_name()] = land 
        return result   


