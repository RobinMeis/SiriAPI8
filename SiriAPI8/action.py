class action: #Stores actions for SiriAPI8
    def __init__ (self):
        self.actions = []
        self.actions.append({'find': "", 'call': self.__error})
        return

    def add (self, find, call): #Add action
        self.actions.append({'find': [find], 'call': call})
        return (len(self.actions) - 1)

    def modify (self, id, find, call): #Modify action by id
        try:
            if (find == -1): #Keep old values if not overwritten
                find = self.actions[id]['find']

            if (call == -1):
                call = self.actions[id]['call']

            self.actions[id] = {'find': [find], 'call': call}
            return (True)
        except:
            return (False)

    def remove (self, id): #Remove action by id
        if (id > 0): #Make it impossible to delete the not found rule
            try:
                del self.actions[id]
                return (True)
            except:
                return (False)
        else:
            return (False)

    def list (self): #List all action
        return (self.actions)

    def __error (self, q, wildcards_found): #Error message if not overwritten
        print ("SiriAPI8 error: No action defined for " + q)
