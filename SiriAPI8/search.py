class search:
    def __init__ (self, SiriAPI):
        self.SiriAPI = SiriAPI

    def search (self, q): #search for matching
        q_search = q.lower().replace(self.SiriAPI.keyword + " ", "")
        for keywords in self.SiriAPI.action.actions[:]: #Complicated search algorithm ;)
            for keyword in keywords['find'][:]:
                for find in keyword[:]:
                    if (isinstance(find, list) == False):
                        if (find == q_search):
                            return (keywords['call'](q, None))
                    else:
                        found = True
                        have_to_follow = True
                        cursor = 0
                        wildcard_counter = -1
                        wildcard_start = 0
                        wildcard_end = -1
                        wildcards_found = {}
                        for search in find[:]:
                            if (search == '*'):
                                wildcard_counter += 1
                                have_to_follow = False
                                wildcard_start = cursor
                            else:
                                position = q_search.find(search, cursor)

                                if (position == cursor):
                                    cursor += len(search) + 1
                                    wildcard_end = position
                                elif (position > cursor and have_to_follow == False):

                                    cursor = position + len(search) + 1
                                    have_to_follow = True
                                    wildcard_end = position - 1
                                else:
                                    found = False
                                    break

                                if (wildcard_end > -1):
                                    wildcards_found[wildcard_counter] = q_search[wildcard_start:wildcard_end]
                                    wildcard_start = 0
                                    wildcard_end = 0

                                if (find[-1] == "*" and find[-2] == search):
                                    wildcards_found[wildcard_counter + 1] = q_search[cursor:]
                                    wildcard_counter += 1


                        if (found == True):
                            return (keywords['call'](q, wildcards_found))
                            return

        return (self.SiriAPI.action.actions[0]['call'](q, None))
