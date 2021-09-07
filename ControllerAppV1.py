import tkinter as tk
from tkinter import ttk
from tkinter import *
import mysql.connector
import matplotlib.pyplot as plt

labelFont =("Verdana",10)

#create a global/helper function to connect to the database
def connect():
    db_session = mysql.connector.connect(
    host = "ec2-54-209-184-86.compute-1.amazonaws.com",
    user = "root",
    password = "comp420",
    database = "cipolitics"
    )
    return db_session
  
#return a specific section of a list
def sliceResults(results,start,end):
    return results[slice( int(start), int(start) + int(end))]

#return a list of entries from x to y
def showXAmount(results):
    resultList = ""
    for currentRow in results:
        resultList += str(currentRow) + "\n"
    return resultList

class tkinterApp(tk.Tk):
    #create each frame and a way to navigate through them
    def __init__(self, *args,**kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure( 0, weight = 1)
        container.grid_columnconfigure( 0, weight = 1)

        self.frames = {}
        #give go through and set each frame
        for currentFrames in (MainFrame, YearFrame, StateFrame, DebateFrame, ConventionFrame,
         PersonFrame, StanceFrame, KeyIssueFrame, MiscellaneousFrame):
            frame = currentFrames(container,self)

            self.frames[currentFrames] = frame

            frame.grid(row =0,column = 0,sticky = "nsew")
    
        self.show_frame(MainFrame)

    #show the frame when the button is clicked
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
class MainFrame(tk.Frame):
    def __init__(self,parent, controller):
        
        tk.Frame.__init__(self,parent)
        
        self.img = tk.PhotoImage( file =r"usflag.png")
        
        picture = Label(self,image = self.img)
        picture.grid(row= 2, column = 2)

        instructionLabel = ttk.Label(self, text = "Welcome to the Policatlly Accurate Database!"
                                            +"\nTo use this database hit the buttons on the left to take you were the magic happens."
                                            +"\nEach frame has all of the atributes that must be filled in to perform an insert."
                                            +"\nFor searches and deletes, all that needs to be provided are the primary IDs."
                                            +"\nThese are the first attibutes in the list."
                                            +"\nFor an update, enter all information required for the update."
                                            +"\nYou must place all the nessary commas, but you are not required to file them all out."
                                            +"\nThe miscellaneous frame has special instructions for it's buttons."
                                            +"\nTo use them, just enter a table in the entry bar and then hit the button."
                                            ,font = labelFont)
        instructionLabel.grid(row = 2, column = 5)

        mainFrameLabel = ttk.Label(self, text = "Politcally Accurate Database", font = labelFont)
        mainFrameLabel.grid(row = 1,column = 2)

        yearFrameButton = ttk.Button(self, text = "Year Frame", command = lambda: controller.show_frame(YearFrame))
        yearFrameButton.grid(row =1, column = 1)

        stateFrameButton = ttk.Button(self, text = "State Frame", command = lambda: controller.show_frame(StateFrame))
        stateFrameButton.grid(row =2, column = 1)

        debateFrameButton = ttk.Button(self, text = "Debate Frame", command = lambda: controller.show_frame(DebateFrame))
        debateFrameButton.grid(row =3, column = 1)

        conventionFrameButton = ttk.Button(self, text = "Convention Frame", command = lambda: controller.show_frame(ConventionFrame))
        conventionFrameButton.grid(row =4, column = 1)

        personFrameButton = ttk.Button(self, text = "Person Frame", command = lambda: controller.show_frame(PersonFrame))
        personFrameButton.grid(row = 7, column = 1)

        stanceFrameButton = ttk.Button(self, text = "Stance Frame", command = lambda: controller.show_frame(StanceFrame))
        stanceFrameButton.grid(row =8, column = 1)

        KeyIssueFrameButton = ttk.Button(self, text = "Issue Frame", command = lambda: controller.show_frame(KeyIssueFrame))
        KeyIssueFrameButton.grid(row =9, column = 1)
        
        miscellaneousFrameButton = ttk.Button(self, text = "Miscellaneous Frame", command = lambda: controller.show_frame(MiscellaneousFrame))
        miscellaneousFrameButton.grid(row =10, column = 1)

class YearFrame(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        #functions
        def yearStringFormat(elect_year, winner):
            return "The election year is " + str(elect_year) + " and the winner of that year is " +  str(winner) + "."

        def insertYear(self,yearEntry):
            db_session = connect()
            sqlCommiter = db_session.cursor()

            splitString = str(yearEntry).split(',')
            elect_year = splitString[0]
            winner = splitString[1]

            try:
                sqlCommiter.execute("INSERT INTO election_year (elect_year, winning_party) VALUES (%s, %s)",(elect_year, winner)) 
                db_session.commit()
                electionYrResultLabel["text"] =  yearStringFormat(elect_year, winner) + " has been inserted."
            except Exception:
                electionYrResultLabel["text"] = "An error has occured, please check if there is a duplicate or input."
            sqlCommiter.close()
            db_session.close()        

        def deleteYear(self,yearEntry):
            session = connect()
            cursor = session.cursor()

            try:
                #delete that entry
                cursor.execute("DELETE FROM election_year WHERE elect_year = \""+ str(yearEntry) + "\"")
                session.commit()
                electionYrResultLabel["text"] = "Entry "+ str(yearEntry) + " has been deleted."
            except Exception:
                electionYrResultLabel["text"] = "Entry "+ str(yearEntry) + " could not be deleted. Please check if it is in the table."
            cursor.close()
            session.close()

        def searchYear(self,yearEntry):
            session = connect()
            cursor = session.cursor()

            try:
                #get that entry
                cursor.execute("SELECT * FROM election_year WHERE elect_year = \""+ str(yearEntry) + "\"")
                result = cursor.fetchall()
            
                for currentRow in result:
                    elect_year = currentRow[0]
                    winner = currentRow[1]

                electionYrResultLabel["text"] = yearStringFormat(elect_year, winner) 
            except Exception:
                electionYrResultLabel["text"] = "Entry "+ str(yearEntry) + " could not be found. Check if it was inserted into the table."
            cursor.close()
            session.close()

        def show10Year(self,start):
            session = connect()
            
            if start == '':
                start = 0

            cursor = session.cursor()
            cursor.execute("SELECT * FROM election_year")
            result = cursor.fetchall()

            resultList = ""
            #get results x for x+y
            sliceResults = result[slice(int(start),int(start) + 10)]
            for currentRow in sliceResults: 
                    elect_year = currentRow[0]
                    winner = currentRow[1]

                    resultList += yearStringFormat(elect_year, winner) + "\n"
                    electionYrResultLabel["text"] = resultList
            
            cursor.close()
            session.close()

        def updateYear(self,yearEntry):
            db_session = connect()
            cursor = db_session.cursor()

            splitString = str(yearEntry).split(',')
            elect_year = splitString[0]
            winner = splitString[1]

            try:
                cursor = db_session.cursor()   
                cursor.execute("SELECT * FROM election_year WHERE elect_year = \""+ elect_year + "\"")
                result = cursor.fetchall()
                for currentRow in result:
                    resultWinner = currentRow[1]

                if winner == '':
                    winner = resultWinner
            
                cursor.execute("UPDATE election_year SET winning_party = \""+ winner +"\" WHERE elect_year = \""+ elect_year + "\"")
                db_session.commit()
                electionYrResultLabel["text"] = yearStringFormat(elect_year, winner) + " has been updated."
            except Exception:
                electionYrResultLabel["text"] = "Entry "+ str(elect_year) + " could not be found. Check if it was inserted into the table."

            db_session.close()
            cursor.close()

        #main buttons
        yearFrameLabel = ttk.Label(self,text = "Election Year Frame", font = labelFont)
        yearFrameLabel.grid(row = 1, column =3)

        yearAtrributeLabel = ttk.Label(self, text = "Values: elect_year, winning_party \nExample: 2016, Republican", font = labelFont)
        yearAtrributeLabel.grid(row = 1, column = 2)

        mainFrameButton = ttk.Button(self, text = "Title", command = lambda: controller.show_frame(MainFrame))
        mainFrameButton.grid(row =1, column = 1)

        stateFrameButton = ttk.Button(self, text = "State Frame", command = lambda: controller.show_frame(StateFrame))
        stateFrameButton.grid(row =2, column = 1)

        debateFrameButton = ttk.Button(self, text = "Debate Frame", command = lambda: controller.show_frame(DebateFrame))
        debateFrameButton.grid(row =3, column = 1)

        conventionFrameButton = ttk.Button(self, text = "Convention Frame", command = lambda: controller.show_frame(ConventionFrame))
        conventionFrameButton.grid(row =4, column = 1)

        personFrameButton = ttk.Button(self, text = "Person Frame", command = lambda: controller.show_frame(PersonFrame))
        personFrameButton.grid(row = 7, column = 1)

        stanceFrameButton = ttk.Button(self, text = "Stance Frame", command = lambda: controller.show_frame(StanceFrame))
        stanceFrameButton.grid(row =8, column = 1)

        KeyIssueFrameButton = ttk.Button(self, text = "Issue Frame", command = lambda: controller.show_frame(KeyIssueFrame))
        KeyIssueFrameButton.grid(row =9, column = 1)

        miscellaneousFrameButton = ttk.Button(self, text = "Miscellaneous Frame", command = lambda: controller.show_frame(MiscellaneousFrame))
        miscellaneousFrameButton.grid(row =10, column = 1)
        
        #entries
        yearInsertEntry = tk.Entry(self, bg= 'white', width = 20)
        yearInsertEntry.grid(row =3, column =2)

        yearDeleteEntry = tk.Entry(self, bg = "white", width = 20)
        yearDeleteEntry.grid(row = 3,column = 3)

        yearSearchEntry = tk.Entry(self, bg = "white", width = 20)
        yearSearchEntry.grid(row = 3, column = 4)

        yearUpdateEntry = tk.Entry(self, bg= 'white', width = 20)
        yearUpdateEntry.grid(row =3, column =5)

        year10SearchEntry = tk.Entry(self,bg = "white", width = 10)
        year10SearchEntry.grid(row = 3, column =6)

        #query buttons
        yearInsertButton = ttk.Button(self, text = "insert",  command = lambda: insertYear(self,yearInsertEntry.get()))
        yearInsertButton.grid(row = 2, column =2)

        yearDeleteButton = ttk.Button(self, text = "delete", command = lambda: deleteYear(self,yearDeleteEntry.get()))
        yearDeleteButton.grid(row = 2, column = 3)

        yearSearchButton = ttk.Button(self, text = "search", command = lambda: searchYear(self,yearSearchEntry.get()))
        yearSearchButton.grid(row = 2, column = 4)

        yearUpdateButton = ttk.Button(self, text = "update", command = lambda: updateYear(self,yearUpdateEntry.get()))
        yearUpdateButton.grid(row =2, column =5)

        year10SearchButton = ttk.Button(self, text = "10 Entries", command = lambda: show10Year(self,year10SearchEntry.get()))
        year10SearchButton.grid(row = 2, column =6)

        #display results
        electionYrResultLabel = tk.Label(self, bg = "white", bd = 10, font =labelFont)
        electionYrResultLabel.grid(row = 5, column = 2)

class StateFrame(tk.Frame):
    def  __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        #functions
        def stateStringFormat(state_id, elect_year, party):
            stateName = ""

            for currentLetter in state_id:
                currentLetter = str(currentLetter).lower()
                if currentLetter in ['a','b,','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']:
                    stateName += currentLetter
            
            stateName = stateName.upper()
            return "The state_id " + str(state_id) +" is " + stateName + " has the year as " + str(elect_year) + " with the winning party " + str(party) 

        def insertState(self,stateEntry):
            db_session = connect()
            sqlCommiter = db_session.cursor()

            splitString = str(stateEntry).split(',')
            state_id = splitString[0]
            elect_year = splitString[1]
            party = splitString[2]

            try:
                sqlCommiter.execute("INSERT INTO state (state_id, elect_year, winner) VALUES (%s, %s, %s)",(state_id, elect_year, party)) 
                db_session.commit()
                stateResultLabel["text"] = stateStringFormat(state_id,elect_year, party) + " has been inserted."
            except Exception:
               stateResultLabel["text"] = "An error has occured, please check if there is a duplicate or input."
            sqlCommiter.close()
            db_session.close()        

        def deleteState(self,stateEntry):
            session = connect()
            cursor = session.cursor()

            try:
                #delete that entry
                cursor.execute("DELETE FROM state WHERE state_id = \""+ str(stateEntry) + "\"")
                session.commit()
                stateResultLabel["text"] = "Entry "+ str(stateEntry) + " has been deleted."
            except Exception:
                stateResultLabel["text"] = "Entry "+ str(stateEntry) + " could not be deleted. Please check if it is in the table."
            cursor.close()
            session.close()

        def searchState(self,stateEntry):
            session = connect()
            cursor = session.cursor()

            try:
                #get that entry
                #cursor.execute("SELECT * FROM state WHERE state_id = \""+ str(stateEntry) + "\"")
                cursor.execute("CALL get_state_by_id(\"" + str(stateEntry) + "\")")
                result = cursor.fetchall()
            
                for currentRow in result:
                    state_id = currentRow[0]
                    elect_year = currentRow[1]
                    party = currentRow[2]

                stateResultLabel["text"] = stateStringFormat(state_id, elect_year, party) + "."
            except Exception:
                stateResultLabel["text"] = "Entry "+ str(stateEntry) + " could not be found. Check if it was inserted into the table."

        def show10States(self,start):
            session = connect()
            
            if start == '':
                start = 0

            cursor = session.cursor()
            cursor.execute("SELECT * FROM state")
            result = cursor.fetchall()

            resultList = ""
            #get results x for x+y
            sliceResults = result[slice(int(start),int(start) + 10)]
            for currentRow in sliceResults: 
                state_id = currentRow[0]
                elect_year = currentRow[1]
                party = currentRow[2]

                resultList += stateStringFormat(state_id, elect_year, party) + "\n"
                stateResultLabel["text"] = resultList
            
            cursor.close()
            session.close()

        def updateState(self,stateEntry):
            db_session = connect()
            cursor = db_session.cursor()

            splitString = str(stateEntry).split(',')
            state_id = splitString[0]
            elect_year = splitString[1]
            party = splitString[2]

            try:
                cursor = db_session.cursor()   
                cursor.execute("SELECT * FROM state where state_id = \"" + state_id + "\"")
                result = cursor.fetchall()
                for currentRow in result:
                    resultElect_year = currentRow[1]
                    resultParty = currentRow[2]

                if elect_year == '':
                    elect_year = resultElect_year
                if party == '':
                    party = resultParty
            
                cursor.execute("UPDATE state SET elect_year = %s, winner = %s WHERE state_id = \""+ state_id + "\"",(elect_year,party))
                db_session.commit()
                stateResultLabel["text"] = stateStringFormat(state_id, elect_year, party) + " has been updated."
            except Exception:
                stateResultLabel["text"] = "Entry "+ str(stateEntry) + " could not be found. Check if it was inserted into the table."

            db_session.close()
            cursor.close()

        #main buttons
        stateFrameLabel = ttk.Label(self,text = "States Frame", font = labelFont)
        stateFrameLabel.grid(row = 1, column =3)

        stateAtrributeLabel = ttk.Label(self, text = "Values: state_id, elect_year, winner \nExample:0016al,2016,Republican", font = labelFont)
        stateAtrributeLabel.grid(row = 1, column = 2)

        yearFrameButton = ttk.Button(self, text = "Year Frame", command = lambda: controller.show_frame(YearFrame))
        yearFrameButton.grid(row =1, column = 1)

        mainFrameButton = ttk.Button(self, text = "Title", command = lambda: controller.show_frame(MainFrame))
        mainFrameButton.grid(row =2, column = 1)

        debateFrameButton = ttk.Button(self, text = "Debate Frame", command = lambda: controller.show_frame(DebateFrame))
        debateFrameButton.grid(row =3, column = 1)

        conventionFrameButton = ttk.Button(self, text = "Convention Frame", command = lambda: controller.show_frame(ConventionFrame))
        conventionFrameButton.grid(row =4, column = 1)

        personFrameButton = ttk.Button(self, text = "Person Frame", command = lambda: controller.show_frame(PersonFrame))
        personFrameButton.grid(row = 7, column = 1)

        stanceFrameButton = ttk.Button(self, text = "Stance Frame", command = lambda: controller.show_frame(StanceFrame))
        stanceFrameButton.grid(row =8, column = 1)

        KeyIssueFrameButton = ttk.Button(self, text = "Issue Frame", command = lambda: controller.show_frame(KeyIssueFrame))
        KeyIssueFrameButton.grid(row =9, column = 1)

        miscellaneousFrameButton = ttk.Button(self, text = "Miscellaneous Frame", command = lambda: controller.show_frame(MiscellaneousFrame))
        miscellaneousFrameButton.grid(row =10, column = 1)

        #entries
        stateInsertEntry = tk.Entry(self, bg= 'white', width = 20)
        stateInsertEntry.grid(row =3, column =2)

        stateDeleteEntry = tk.Entry(self, bg = "white", width = 20)
        stateDeleteEntry.grid(row = 3,column = 3)

        stateSearchEntry = tk.Entry(self, bg = "white", width = 20)
        stateSearchEntry.grid(row = 3, column = 4)

        stateUpdateEntry = tk.Entry(self, bg= 'white', width = 20)
        stateUpdateEntry.grid(row =3, column =5)
        
        state10SearchEntry = tk.Entry(self,bg = "white", width = 10)
        state10SearchEntry.grid(row = 3, column =6)

        #query buttons
        stateInsertButton = ttk.Button(self, text = "insert",  command = lambda: insertState(self,stateInsertEntry.get()))
        stateInsertButton.grid(row = 2, column =2)

        stateDeleteButton = ttk.Button(self, text = "delete", command = lambda: deleteState(self,stateDeleteEntry.get()))
        stateDeleteButton.grid(row = 2, column = 3)

        stateSearchButton = ttk.Button(self, text = "search", command = lambda: searchState(self,stateSearchEntry.get()))
        stateSearchButton.grid(row = 2, column = 4)

        stateUpdateButton = ttk.Button(self, text = "update", command = lambda: updateState(self,stateUpdateEntry.get()))
        stateUpdateButton.grid(row =2, column =5)

        state10SearchButton = ttk.Button(self, text = "10 Entries", command = lambda: show10States(self,state10SearchEntry.get()))
        state10SearchButton.grid(row = 2, column =6)

        #resultFrame/label
        stateResultLabel = tk.Label(self, bg = "white", bd = 10,font = labelFont)
        stateResultLabel.grid(row = 5, column = 2)

class DebateFrame(tk.Frame):
    def  __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        #functions
        def debateStringFormat(debate_id, elect_year, republican, democrat, debate_type, place):
            viceOrPres = ''
            if str(debate_type) == 'pr':
                viceOrPres += "presidential debate"
            else:
                viceOrPres += "vice presidential debate"

            return str(debate_id) + " took place in the year " + str(elect_year) + " at " + str(place) + " with " + str(democrat) + " and " + str(republican) + " doing a " + viceOrPres 

        def insertDebate(self,debateEntry):
            db_session = connect()
            sqlCommiter = db_session.cursor()

            
            maxSplit = 5
            splitString = str(debateEntry).split(',',maxSplit)
            debate_id = splitString[0]
            elect_year = splitString[1]
            republican = splitString[2]
            democrat = splitString[3]
            debate_type = splitString[4]
            place = splitString[5]

            try:
                sqlCommiter.execute("INSERT INTO debate (debate_id, elect_year, republican_candidate, democrat_candidate, debate_type,place) VALUES (%s, %s, %s, %s, %s, %s)",(debate_id, elect_year, republican, democrat, debate_type, place)) 
                db_session.commit()
                debateResultLabel["text"] =  debateStringFormat(debate_id, elect_year, republican, democrat, debate_type, place) + " has been inserted."
            except Exception:
                debateResultLabel["text"] = "An error has occured, please check if there is a duplicate or input."
            sqlCommiter.close()
            db_session.close()        

        def deleteDebate(self,debateEntry):
            session = connect()
            cursor = session.cursor()

            try:
                #delete that entry
                #cursor.execute("DELETE FROM debate WHERE debate_id = \""+ str(debateEntry) + "\"")
                cursor.execute("CALL delete_debate(\""+ str(debateEntry) +"\")")
                session.commit()
                debateResultLabel["text"] = "Entry "+ str(debateEntry) + " has been deleted."
            except Exception:
                debateResultLabel["text"] = "Entry "+ str(debateEntry) + " could not be deleted. Please check if it is in the table."
            cursor.close()
            session.close()

        def searchDebate(self,debateEntry):
            session = connect()
            cursor = session.cursor()

            try:
                #get that entry
                #cursor.execute("SELECT * FROM debate WHERE debate_id = \""+ str(debateEntry) + "\"")
                cursor.execute("CALL get_debate_by_id(\""+ str(debateEntry) +"\")")
                result = cursor.fetchall()
                
                for currentRow in result:
                    debate_id = currentRow[0]
                    elect_year = currentRow[1]
                    republican = currentRow[2]
                    democrat = currentRow[3]
                    debate_type = currentRow[4]
                    place = currentRow[5]

                debateResultLabel["text"] = debateStringFormat(debate_id, elect_year, republican, democrat, debate_type, place)+"."
            except Exception:
                debateResultLabel["text"] = "Entry "+ str(debateEntry) + " could not be found. Check if it was inserted into the table."
            cursor.close()
            session.close()

        def show10Debate(self,start):
            session = connect()
            
            if start == '':
                start = 0

            cursor = session.cursor()
            cursor.execute("SELECT * FROM debate")
            result = cursor.fetchall()

            resultList = ""
            #get results x for x+y
            sliceResults = result[slice(int(start),int(start) + 10)]
            for currentRow in sliceResults: 
                    debate_id = currentRow[0]
                    elect_year = currentRow[1]
                    republican = currentRow[2]
                    democrat = currentRow[3]
                    debate_type = currentRow[4]
                    place = currentRow[5]

                    resultList += debateStringFormat(debate_id, elect_year, republican, democrat, debate_type, place) + "\n"
                    debateResultLabel["text"] = resultList
            
            cursor.close()
            session.close()

        def updateDebate(self,debateEntry): 
            db_session = connect()
            cursor = db_session.cursor()

            maxSplit = 5
            splitString = str(debateEntry).split(',',maxSplit)
            debate_id = splitString[0]
            elect_year = splitString[1]
            republican = splitString[2]
            democrat = splitString[3]
            debate_type = splitString[4]
            place = splitString[5]

            try:
                cursor = db_session.cursor()   
                cursor.execute("SELECT * FROM debate WHERE debate_id = \""+ debate_id + "\"")
                result = cursor.fetchall()
                for currentRow in result:
                    resultElect_year = currentRow[1]
                    resultRepublican = currentRow[2]
                    resultDemocrat = currentRow[3]
                    resultDebate_type = currentRow[4]
                    resultPlace = currentRow[5]

                if elect_year == '':
                    elect_year = resultElect_year
                if republican == '':
                    republican = resultRepublican
                if democrat == '':
                    democrat = resultDemocrat
                if debate_type =='':
                    debate_type = resultDebate_type
                if place == '': 
                    place = resultPlace
            
                cursor.execute("UPDATE debate SET elect_year = %s,republican_candidate = %s, democrat_candidate = %s, debate_type =%s, place = %s WHERE debate_id = \""+ debate_id + "\"",
                (elect_year, republican, democrat, debate_type, place))
                db_session.commit()
                debateResultLabel["text"] = debateStringFormat(debate_id, elect_year, republican, democrat, debate_type, place)+" has been updated."
            except Exception:
                debateResultLabel["text"] = "Entry "+ str(debateEntry) + " could not be found. Check if it was inserted into the table."
            
            db_session.close()
            cursor.close()

        # Main buttons
        debateFrameLabel = ttk.Label(self,text = "Debates Frame", font = labelFont)
        debateFrameLabel.grid(row = 1, column =3)

        debateAtrributeLabel = ttk.Label(self, text = "Values: debate_id, elect_year, republican_candidate, democrat_candidate,debate_type,place "
                                                    +"\nExample: 16pr1, 2016, trump16, clinton16, pr, Hofstra University NY"
                                                    +"\nBoth repupblican and democratic candidate are person_ids."
                                                    , font = labelFont)
        debateAtrributeLabel.grid(row = 1, column = 2)

        yearFrameButton = ttk.Button(self, text = "Year Frame", command = lambda: controller.show_frame(YearFrame))
        yearFrameButton.grid(row =1, column = 1)

        stateFrameButton = ttk.Button(self, text = "State Frame", command = lambda: controller.show_frame(StateFrame))
        stateFrameButton.grid(row =2, column = 1)

        mainFrameButton = ttk.Button(self, text = "Title", command = lambda: controller.show_frame(MainFrame))
        mainFrameButton.grid(row =3, column = 1)

        conventionFrameButton = ttk.Button(self, text = "Convention Frame", command = lambda: controller.show_frame(ConventionFrame))
        conventionFrameButton.grid(row =4, column = 1)

        personFrameButton = ttk.Button(self, text = "Person Frame", command = lambda: controller.show_frame(PersonFrame))
        personFrameButton.grid(row = 7, column = 1)

        stanceFrameButton = ttk.Button(self, text = "Stance Frame", command = lambda: controller.show_frame(StanceFrame))
        stanceFrameButton.grid(row =8, column = 1)

        KeyIssueFrameButton = ttk.Button(self, text = "Issue Frame", command = lambda: controller.show_frame(KeyIssueFrame))
        KeyIssueFrameButton.grid(row =9, column = 1)

        miscellaneousFrameButton = ttk.Button(self, text = "Miscellaneous Frame", command = lambda: controller.show_frame(MiscellaneousFrame))
        miscellaneousFrameButton.grid(row =10, column = 1)
        
        #entries
        debateInsertEntry = tk.Entry(self, bg= 'white', width = 55)
        debateInsertEntry.grid(row =3, column =2)

        debateDeleteEntry = tk.Entry(self, bg = "white", width = 20)
        debateDeleteEntry.grid(row = 3,column = 3)

        debateSearchEntry = tk.Entry(self, bg = "white", width = 20)
        debateSearchEntry.grid(row = 3, column = 4)

        debateUpdateEntry = tk.Entry(self, bg= 'white', width = 60)
        debateUpdateEntry.grid(row =3, column =5)

        debate10SearchEntry = tk.Entry(self,bg = "white", width = 10)
        debate10SearchEntry.grid(row = 3, column =6)

        #query buttons
        debateInsertButton = ttk.Button(self, text = "insert",  command = lambda: insertDebate(self,debateInsertEntry.get()))
        debateInsertButton.grid(row = 2, column =2)

        debateDeleteButton = ttk.Button(self, text = "delete", command = lambda: deleteDebate(self,debateDeleteEntry.get()))
        debateDeleteButton.grid(row = 2, column = 3)

        debateSearchButton = ttk.Button(self, text = "search", command = lambda: searchDebate(self,debateSearchEntry.get()))
        debateSearchButton.grid(row = 2, column = 4)

        debateUpdateButton = ttk.Button(self, text = "update", command = lambda: updateDebate(self,debateUpdateEntry.get()))
        debateUpdateButton.grid(row =2, column =5)

        debate10SearchButton = ttk.Button(self, text = "10 Entries", command = lambda: show10Debate(self,debate10SearchEntry.get()))
        debate10SearchButton.grid(row = 2, column =6)

        #display results
        debateResultLabel = tk.Label(self, bg = "white", bd = 10, font = labelFont)
        debateResultLabel.grid(row = 5, column = 2)

class ConventionFrame(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        def conventionStringFormat(convention_id, elect_year, party, person_id, place):
            return "The convention_id "+ str(convention_id) + " took place in the year " + str(elect_year) + ".\n " + str(person_id) + " being the presidential nonination for the party "+ str(party) + " at " + str(place)

        def insertConvention(self,conventionEntry):
            db_session = connect()
            sqlCommiter = db_session.cursor()

            splitString = str(conventionEntry).split(',',5)
            convention_id = splitString[0]
            elect_year = splitString[1]
            party = splitString[2]
            person_id = splitString[3]
            place = splitString[4]

            try:
                sqlCommiter.execute("INSERT INTO convention (convention_id, elect_year, party, person_id,place) VALUES (%s, %s, %s, %s,%s)",
                (convention_id, elect_year, party, person_id, place)) 
                db_session.commit()
                conventionResultLabel["text"] = conventionStringFormat(convention_id, elect_year, party, person_id,place) + " has been inserted."
            except Exception:
                conventionResultLabel["text"] = "An error has occured, please check if there is a duplicate or input."
            sqlCommiter.close()
            db_session.close()        

        def deleteConvention(self,conventionEntry):
            session = connect()
            cursor = session.cursor()

            try:
                #delete that entry
                #cursor.execute("DELETE FROM convention WHERE convention_id = \""+ str(conventionEntry) + "\"")
                cursor.execute("CALL delete_convention(\"" +str(conventionEntry) +"\")")
                session.commit()
                conventionResultLabel["text"] = "Entry "+ str(conventionEntry) + " has been deleted."
            except Exception:
                conventionResultLabel["text"] = "Entry "+ str(conventionEntry) + " could not be deleted. Please check if it is in the table."
            cursor.close()
            session.close()

        def searchConvention(self,conventionEntry):
            session = connect()
            cursor = session.cursor()

            try:
                #get that entry
                cursor.execute("SELECT * FROM convention WHERE convention_id = \""+ str(conventionEntry) + "\"")
                result = cursor.fetchall()
            
                for currentRow in result:
                    convention_id = currentRow[0]
                    elect_year = currentRow[1]
                    party = currentRow[2]
                    person_id = currentRow[3]
                    place = currentRow[4]

                conventionResultLabel["text"] = conventionStringFormat(convention_id, elect_year, party, person_id,place) + "."
            except Exception:
                conventionResultLabel["text"] = "Entry "+ str(conventionEntry) + " could not be found. Check if it was inserted into the table."
            cursor.close()
            session.close()

        def show10Convention(self,start):
            session = connect()
            
            if start == '':
                start = 0

            cursor = session.cursor()
            cursor.execute("SELECT * FROM convention")
            result = cursor.fetchall()

            resultList = ""
            #get results x for x+y
            sliceResults = result[slice(int(start),int(start) + 10)]
            for currentRow in sliceResults: 
                    convention_id = currentRow[0]
                    elect_year = currentRow[1]
                    party = currentRow[2]
                    person_id = currentRow[3]
                    place = currentRow[4]

                    resultList += conventionStringFormat(convention_id, elect_year, party, person_id,place) + "\n"
                    conventionResultLabel["text"] = resultList
            
            cursor.close()
            session.close()

        def updateConvention(self,conventionEntry): 
            db_session = connect()
            cursor = db_session.cursor()

            maxSplit = 4
            splitString = str(conventionEntry).split(',',maxSplit)
            convention_id = splitString[0]
            elect_year = splitString[1]
            party = splitString[2]
            person_id = splitString[3]
            place = splitString[4]

            try:
                cursor = db_session.cursor()   
                cursor.execute("SELECT * FROM convention WHERE convention_id = \""+ str(convention_id) + "\"")
                result = cursor.fetchall()
                for currentRow in result:
                    resultElect_year = currentRow[1]
                    resultParty = currentRow[2]
                    resultPerson_id = currentRow[3]
                    resultPlace = currentRow[4]

                if elect_year == '':
                    elect_year = resultElect_year
                if party == '':
                    party = resultParty
                if person_id == '':
                    person_id = resultPerson_id
                if place == '': 
                    place = resultPlace
    
                cursor.execute("UPDATE convention SET elect_year = %s,party = %s, person_id =%s, place = %s WHERE convention_id = \""+ convention_id + "\"",
                (elect_year, party, person_id,place))
                db_session.commit()
                conventionResultLabel["text"] = conventionStringFormat(convention_id, elect_year, party, person_id,place)+" has been updated."
            except Exception:
                conventionResultLabel["text"] = "Entry "+ str(convention_id) + " could not be found. Check if it was inserted into the table."
            
            db_session.close()
            cursor.close()

        conventionFrameLabel = ttk.Label(self, text = "Convention Frame", font = labelFont)
        conventionFrameLabel.grid(row = 1,column = 3)

        conventionAtrributeLabel = ttk.Label(self, text = "Values: convention_id, elect_year, party, person_id, place "
                                                        +"\nExample: 0016d, 2016, Democrat, clinton16, Philadelphia, Pennsylvania", font = labelFont)
        conventionAtrributeLabel.grid(row = 1, column = 2)

        yearFrameButton = ttk.Button(self, text = "Year Frame", command = lambda: controller.show_frame(YearFrame))
        yearFrameButton.grid(row =1, column = 1)

        stateFrameButton = ttk.Button(self, text = "State Frame", command = lambda: controller.show_frame(StateFrame))
        stateFrameButton.grid(row =2, column = 1)

        debateFrameButton = ttk.Button(self, text = "Debate Frame", command = lambda: controller.show_frame(DebateFrame))
        debateFrameButton.grid(row =3, column = 1)

        mainFrameButton = ttk.Button(self, text = "Title", command = lambda: controller.show_frame(MainFrame))
        mainFrameButton.grid(row =4, column = 1)

        personFrameButton = ttk.Button(self, text = "Person Frame", command = lambda: controller.show_frame(PersonFrame))
        personFrameButton.grid(row = 7, column = 1)

        stanceFrameButton = ttk.Button(self, text = "Stance Frame", command = lambda: controller.show_frame(StanceFrame))
        stanceFrameButton.grid(row =8, column = 1)

        KeyIssueFrameButton = ttk.Button(self, text = "Issue Frame", command = lambda: controller.show_frame(KeyIssueFrame))
        KeyIssueFrameButton.grid(row =9, column = 1)

        miscellaneousFrameButton = ttk.Button(self, text = "Miscellaneous Frame", command = lambda: controller.show_frame(MiscellaneousFrame))
        miscellaneousFrameButton.grid(row =10, column = 1)
        
        #entries
        conventionInsertEntry = tk.Entry(self, bg= 'white', width = 40)
        conventionInsertEntry.grid(row =3, column =2)

        conventionDeleteEntry = tk.Entry(self, bg = "white", width = 20)
        conventionDeleteEntry.grid(row = 3,column = 3)

        conventionSearchEntry = tk.Entry(self, bg = "white", width = 20)
        conventionSearchEntry.grid(row = 3, column = 4)

        conventionUpdateEntry = tk.Entry(self, bg= 'white', width = 60)
        conventionUpdateEntry.grid(row =3, column =5)

        convention10SearchEntry = tk.Entry(self,bg = "white", width = 10)
        convention10SearchEntry.grid(row = 3, column = 6)

        #query buttons
        conventionInsertButton = ttk.Button(self, text = "insert",  command = lambda: insertConvention(self,conventionInsertEntry.get()))
        conventionInsertButton.grid(row = 2, column =2)

        conventionDeleteButton = ttk.Button(self, text = "delete", command = lambda: deleteConvention(self,conventionDeleteEntry.get()))
        conventionDeleteButton.grid(row = 2, column = 3)

        conventionSearchButton = ttk.Button(self, text = "search", command = lambda: searchConvention(self,conventionSearchEntry.get()))
        conventionSearchButton.grid(row = 2, column = 4)

        conventionUpdateButton = ttk.Button(self, text = "update", command = lambda: updateConvention(self,conventionUpdateEntry.get()))
        conventionUpdateButton.grid(row =2, column =5)

        convention10SearchButton = ttk.Button(self, text = "10 Entries", command = lambda: show10Convention(self,convention10SearchEntry.get()))
        convention10SearchButton.grid(row = 2, column =6)

        #display results
        conventionResultLabel = tk.Label(self, bg = "white", bd = 10, font = labelFont)
        conventionResultLabel.grid(row = 5, column = 2)

class PersonFrame(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        #functions
        def personStringFormat(person_id, person_name, party, person_title, elect_year, stance_id, endorsed):
            printString = "The person_id is "+ str(person_id) + " is " + str(person_name) + " and are part of the " + str(party) + " party in the year " + str(elect_year) + ".\n" +"They are the " + str(person_title)
            if person_title == "Presidential Candidate" or person_title == "Vice Presidential Candidate" or person_title == "Vice President": 
                printString += " and have a stance_id " + str(stance_id)
            else:
                printString += " and are endorsing " + str(endorsed)

            return printString  

        def insertPerson(self,personEntry):
            db_session = connect()
            sqlCommiter = db_session.cursor()

            splitString = str(personEntry).split(',')
            person_id = splitString[0]
            person_name = splitString[1]
            party= splitString[2]
            person_title = splitString[3]
            elect_year = splitString[4]
            stance_id = splitString[5]
            endorsed = splitString[6]

            try:
                sqlCommiter.execute("INSERT INTO person (person_id, person_name, party, person_title, elect_year, stance_id, endorsed) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (person_id, person_name, party, person_title, elect_year, stance_id, endorsed)) 
                db_session.commit()
                personResultLabel["text"] = personStringFormat(person_id, person_name, party, person_title, elect_year, stance_id, endorsed) + " has been inserted."
            except Exception:
                personResultLabel["text"] = "An error has occured, please check if there is a duplicate or input."
            sqlCommiter.close()
            db_session.close()        

        def deletePerson(self,personEntry):
            session = connect()
            cursor = session.cursor()

            try:
                #delete that entry
                #cursor.execute("DELETE FROM person WHERE person_id = \""+ str(personEntry) + "\"")
                cursor.execute("CALL delete_person(\"" + str(personEntry )+"\")")
                session.commit()
                personResultLabel["text"] = "Entry "+ str(personEntry) + " has been deleted."
            except Exception:
                personResultLabel["text"] = "Entry "+ str(personEntry) + " could not be deleted. Please check if it is in the table."
            cursor.close()
            session.close()

        def searchPerson(self,personEntry):
            session = connect()
            cursor = session.cursor()

            try:
                #get that entry
                cursor.execute("SELECT * FROM person WHERE person_id = \""+ str(personEntry) + "\"")
                result = cursor.fetchall()
            
                for currentRow in result:
                    person_id = currentRow[0]
                    person_name = currentRow[1]
                    party = currentRow[2]
                    person_title = currentRow[3]
                    elect_year = currentRow[4]
                    stance_id = currentRow[5]
                    endorsed = currentRow[6]

                personResultLabel["text"] = personStringFormat(person_id, person_name, party, person_title, elect_year, stance_id, endorsed) + "."
            except Exception:
                personResultLabel["text"] = "Entry "+ str(personEntry) + " could not be found. Check if it was inserted into the table."
            cursor.close()
            session.close()

        def show10Person(self,start):
            session = connect()
            
            if start == '':
                start = 0

            cursor = session.cursor()
            cursor.execute("SELECT * FROM person")
            result = cursor.fetchall()

            resultList = ""
            #get results x for x+y
            sliceResults = result[slice(int(start),int(start) + 10)]
            for currentRow in sliceResults: 
                    person_id = currentRow[0]
                    person_name = currentRow[1]
                    party = currentRow[2]
                    person_title = currentRow[3]
                    elect_year = currentRow[4]
                    stance_id = currentRow[5]
                    endorsed = currentRow[6]

                    resultList += personStringFormat(person_id, person_name, party, person_title, elect_year, stance_id, endorsed) + "\n"
                    personResultLabel["text"] = resultList
            
            cursor.close()
            session.close()

        def updatePerson(self,personEntry): 
            db_session = connect()
            cursor = db_session.cursor()

            splitString = str(personEntry).split(',')
            person_id = splitString[0]
            person_name = splitString[1]
            party= splitString[2]
            person_title = splitString[3]
            elect_year = splitString[4]
            stance_id = splitString[5]
            endorsed = splitString[6]

            try:
                cursor = db_session.cursor()   
                cursor.execute("SELECT * FROM person WHERE person_id = \""+ str(person_id) + "\"")
                result = cursor.fetchall()
                for currentRow in result:
                    resultPerson_name = currentRow[1]
                    resultParty = currentRow[2]
                    resultPerson_title = currentRow[3]
                    resultElect_year = currentRow[4]
                    resultStance_id = currentRow[5]
                    resultEndorsed = currentRow[6]

                if elect_year == '':
                    elect_year = resultElect_year
                if party == '':
                    party = resultParty
                if person_title == '': 
                    person_title = resultPerson_title
                if elect_year == '':
                    elect_year = resultElect_year
                if stance_id == '':
                    stance_id = resultStance_id
                if endorsed == '':
                    endorsed = resultEndorsed
                if person_name =='':
                    person_name = resultPerson_name
    
                cursor.execute("UPDATE person SET person_name =%s, party = %s, person_title= %s, elect_year = %s,stance_id = %s, endorsed =%s WHERE person_id = \""+ person_id + "\"",
                (person_name, party, person_title, elect_year, stance_id, endorsed))
                db_session.commit()
                personResultLabel["text"] = personStringFormat(person_id, person_name, party, person_title, elect_year, stance_id, endorsed)+" has been updated."
            except Exception:
                personResultLabel["text"] = "Entry "+ str(person_id) + " could not be found. Check if it was inserted into the table."
            
            db_session.close()
            cursor.close()

        personFrameLabel = ttk.Label(self, text = "Person Frame",font = labelFont)
        personFrameLabel.grid(row = 1,column = 3)

        personAtrributeLabel = ttk.Label(self, text = "Values: person_id, person_name, party, person_title, elect_year, stance_id, endorsed "
                                                        +"\nExample:pence16, Mike Pence, Republican, Vice Presidential Candidate, 2016, 0, presidential candidate" 
                                                        , font = labelFont)
        personAtrributeLabel.grid(row = 1, column = 2)

        yearFrameButton = ttk.Button(self, text = "Year Frame", command = lambda: controller.show_frame(YearFrame))
        yearFrameButton.grid(row =1, column = 1)

        stateFrameButton = ttk.Button(self, text = "State Frame", command = lambda: controller.show_frame(StateFrame))
        stateFrameButton.grid(row =2, column = 1)

        debateFrameButton = ttk.Button(self, text = "Debate Frame", command = lambda: controller.show_frame(DebateFrame))
        debateFrameButton.grid(row =3, column = 1)

        conventionFrameButton = ttk.Button(self, text = "Convention Frame", command = lambda: controller.show_frame(ConventionFrame))
        conventionFrameButton.grid(row =4, column = 1)

        mainFrameButton = ttk.Button(self, text = "Title", command = lambda: controller.show_frame(MainFrame))
        mainFrameButton.grid(row = 7, column = 1)

        stanceFrameButton = ttk.Button(self, text = "Stance Frame", command = lambda: controller.show_frame(StanceFrame))
        stanceFrameButton.grid(row = 8, column = 1)

        KeyIssueFrameButton = ttk.Button(self, text = "Issue Frame", command = lambda: controller.show_frame(KeyIssueFrame))
        KeyIssueFrameButton.grid(row = 9, column = 1)

        miscellaneousFrameButton = ttk.Button(self, text = "Miscellaneous Frame", command = lambda: controller.show_frame(MiscellaneousFrame))
        miscellaneousFrameButton.grid(row =10, column = 1)

        #entries
        personInsertEntry = tk.Entry(self, bg= 'white', width = 60)
        personInsertEntry.grid(row =3, column =2)

        personDeleteEntry = tk.Entry(self, bg = "white", width = 20)
        personDeleteEntry.grid(row = 3,column = 3)

        personSearchEntry = tk.Entry(self, bg = "white", width = 20)
        personSearchEntry.grid(row = 3, column = 4)

        personUpdateEntry = tk.Entry(self, bg= 'white', width = 60)
        personUpdateEntry.grid(row =3, column =5)

        person10SearchEntry = tk.Entry(self,bg = "white", width = 10)
        person10SearchEntry.grid(row = 3, column =6)

        #query buttons
        personInsertButton = ttk.Button(self, text = "insert",  command = lambda: insertPerson(self,personInsertEntry.get()))
        personInsertButton.grid(row = 2, column =2)

        personDeleteButton = ttk.Button(self, text = "delete", command = lambda: deletePerson(self,personDeleteEntry.get()))
        personDeleteButton.grid(row = 2, column = 3)

        personSearchButton = ttk.Button(self, text = "search", command = lambda: searchPerson(self,personSearchEntry.get()))
        personSearchButton.grid(row = 2, column = 4)

        personUpdateButton = ttk.Button(self, text = "update", command = lambda: updatePerson(self,personUpdateEntry.get()))
        personUpdateButton.grid(row =2, column =5)

        person10SearchButton = ttk.Button(self, text = "10 Entries", command = lambda: show10Person(self,person10SearchEntry.get()))
        person10SearchButton.grid(row = 2, column =6)

        #display results
        personResultLabel = tk.Label(self, bg = "white", bd = 10)
        personResultLabel.grid(row = 5, column = 2)

class StanceFrame(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        #functions
        def stanceStringFormat(stance_id, issue_id, position):
            return "stance_id " + str(stance_id) + " has issue_id " + str(issue_id) + " and has the postion " + str(position) + " on this stance."

        def insertStance(self,stanceEntry):
            db_session = connect()
            sqlCommiter = db_session.cursor()

            splitString = str(stanceEntry).split(',',5)
            stance_id = splitString[0]
            issue_id = splitString[1]
            position= splitString[2]

            try:
                sqlCommiter.execute("INSERT INTO stance (stance_id, issue_id, position) VALUES (%s, %s, %s)",
                (stance_id, issue_id, position)) 
                db_session.commit()
                stanceResultLabel["text"] = stanceStringFormat(stance_id, issue_id, position) + " has been inserted."
            except Exception:
                stanceResultLabel["text"] = "An error has occured, please check if there is a duplicate or input."
            sqlCommiter.close()
            db_session.close()        

        def deleteStance(self,stanceEntry):
            session = connect()
            cursor = session.cursor()

            try:
                #delete that entry
                cursor.execute("DELETE FROM stance WHERE stance_id = \""+ str(stanceEntry) + "\"")
                session.commit()
                stanceResultLabel["text"] = "Entry "+ str(stanceEntry) + " has been deleted."
            except Exception:
                stanceResultLabel["text"] = "Entry "+ str(stanceEntry) + " could not be deleted. Please check if it is in the table."
            cursor.close()
            session.close()

        def searchStance(self,stanceEntry):
            session = connect()
            cursor = session.cursor()

            try:
                #get that entry
                cursor.execute("SELECT * FROM stance WHERE stance_id = \""+ str(stanceEntry) + "\"")
                result = cursor.fetchall()
            
                for currentRow in result:
                    stance_id = currentRow[0]
                    issue_id = currentRow[1]
                    position = currentRow[2]

                stanceResultLabel["text"] = stanceStringFormat(stance_id, issue_id, position) + "."
            except Exception:
                stanceResultLabel["text"] = "Entry "+ str(stanceEntry) + " could not be found. Check if it was inserted into the table."
            cursor.close()
            session.close()

        def show10Stance(self,start):
            session = connect()
            
            if start == '':
                start = 0

            cursor = session.cursor()
            cursor.execute("SELECT * FROM stance")
            result = cursor.fetchall()

            resultList = ""
            #get results x for x+y
            sliceResults = result[slice(int(start),int(start) + 10)]
            for currentRow in sliceResults: 
                    stance_id = currentRow[0]
                    issue_id = currentRow[1]
                    position = currentRow[2]
                    
                    resultList += stanceStringFormat(stance_id, issue_id, position) + "\n"
                    stanceResultLabel["text"] = resultList
            
            cursor.close()
            session.close()

        def updateStance(self,stanceEntry): 
            db_session = connect()
            cursor = db_session.cursor()

            splitString = str(stanceEntry).split(',')
            stance_id = splitString[0]
            issue_id = splitString[1]
            position= splitString[2]

            try:
                cursor = db_session.cursor()   
                cursor.execute("SELECT * FROM stance WHERE stance_id = \""+ str(stanceEntry) + "\"")
                result = cursor.fetchall()
                for currentRow in result:
                    resultIssue_id = currentRow[1]
                    resultPosition = currentRow[2]

                if issue_id == '':
                    issue_id = resultIssue_id
                if position == '':
                    position = resultPosition

                cursor.execute("UPDATE stance SET issue_id =%s, position = %s WHERE stance_id = \""+ stance_id + "\"",
                (issue_id, position))
                db_session.commit()
                stanceResultLabel["text"] = stanceStringFormat(stance_id, issue_id, position)+" has been updated."
            except Exception:
                stanceResultLabel["text"] = "Entry "+ str(stance_id) + " could not be found. Check if it was inserted into the table."
            
            db_session.close()
            cursor.close()

        stanceFrameLabel = ttk.Label(self, text = "Stance Frame",font = labelFont)
        stanceFrameLabel.grid(row = 1,column = 3)

        stanceAtrributeLabel = ttk.Label(self, text = "Values: stance_id, issue_id, position "
                                                        +"\nExample: 0, 0, against",
                                                         font = labelFont)
        stanceAtrributeLabel.grid(row = 1, column = 2)

        yearFrameButton = ttk.Button(self, text = "Year Frame", command = lambda: controller.show_frame(YearFrame))
        yearFrameButton.grid(row =1, column = 1)

        stateFrameButton = ttk.Button(self, text = "State Frame", command = lambda: controller.show_frame(StateFrame))
        stateFrameButton.grid(row =2, column = 1)

        debateFrameButton = ttk.Button(self, text = "Debate Frame", command = lambda: controller.show_frame(DebateFrame))
        debateFrameButton.grid(row =3, column = 1)

        conventionFrameButton = ttk.Button(self, text = "Convention Frame", command = lambda: controller.show_frame(ConventionFrame))
        conventionFrameButton.grid(row =4, column = 1)

        personFrameButton = ttk.Button(self, text = "Person Frame", command = lambda: controller.show_frame(PersonFrame))
        personFrameButton.grid(row =7, column = 1)
        
        mainFrameButton = ttk.Button(self, text = "Title", command = lambda: controller.show_frame(MainFrame))
        mainFrameButton.grid(row =8, column = 1)

        keyIssueFrameButton = ttk.Button(self, text = "Issue Frame", command = lambda: controller.show_frame(KeyIssueFrame))
        keyIssueFrameButton.grid(row = 9, column = 1)

        miscellaneousFrameButton = ttk.Button(self, text = "Miscellaneous Frame", command = lambda: controller.show_frame(MiscellaneousFrame))
        miscellaneousFrameButton.grid(row =10, column = 1)

        #entries
        stanceInsertEntry = tk.Entry(self, bg= 'white', width = 40)
        stanceInsertEntry.grid(row =3, column =2)

        stanceDeleteEntry = tk.Entry(self, bg = "white", width = 20)
        stanceDeleteEntry.grid(row = 3,column = 3)

        stanceSearchEntry = tk.Entry(self, bg = "white", width = 20)
        stanceSearchEntry.grid(row = 3, column = 4)

        stanceUpdateEntry = tk.Entry(self, bg= 'white', width = 60)
        stanceUpdateEntry.grid(row =3, column =5)

        stance10SearchEntry = tk.Entry(self,bg = "white", width = 10)
        stance10SearchEntry.grid(row = 3, column =6)

        #query buttons
        stanceInsertButton = ttk.Button(self, text = "insert",  command = lambda: insertStance(self,stanceInsertEntry.get()))
        stanceInsertButton.grid(row = 2, column =2)

        stanceDeleteButton = ttk.Button(self, text = "delete", command = lambda: deleteStance(self,stanceDeleteEntry.get()))
        stanceDeleteButton.grid(row = 2, column = 3)

        stanceSearchButton = ttk.Button(self, text = "search", command = lambda: searchStance(self,stanceSearchEntry.get()))
        stanceSearchButton.grid(row = 2, column = 4)

        stanceUpdateButton = ttk.Button(self, text = "update", command = lambda: updateStance(self,stanceUpdateEntry.get()))
        stanceUpdateButton.grid(row =2, column =5)

        stance10SearchButton = ttk.Button(self, text = "10 Entries", command = lambda: show10Stance(self,stance10SearchEntry.get()))
        stance10SearchButton.grid(row = 2, column =6)

        #display results
        stanceResultLabel = tk.Label(self, bg = "white", bd = 10, font = labelFont)
        stanceResultLabel.grid(row = 5, column = 2)


class KeyIssueFrame(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        #function
        def keyIssueStringFormat(issue_id,issue_name,issue_description):
            return "issue_id " + str(issue_id) + " is " + str(issue_name) + " with the description " + str(issue_description) + "."

        def insertKeyIssue(self,keyIssueEntry):
            db_session = connect()
            sqlCommiter = db_session.cursor()

            splitString = str(keyIssueEntry).split(',')
            issue_id = splitString[0]
            issue_name = splitString[1]
            issue_description = splitString[2]

            try:
                sqlCommiter.execute("INSERT INTO issues (issue_id, issue_name, issue_description) VALUES (%s, %s, %s)",
                (issue_id, issue_name, issue_description)) 
                db_session.commit()
                keyIssueResultLabel["text"] = keyIssueStringFormat(issue_id, issue_name, issue_description) + " has been inserted."
            except Exception:
                keyIssueResultLabel["text"] = "An error has occured, please check if there is a duplicate or input."
            sqlCommiter.close()
            db_session.close()        

        def deleteKeyIssue(self,keyIssueEntry):
            session = connect()
            cursor = session.cursor()

            try:
                #delete that entry
                cursor.execute("DELETE FROM issues WHERE issue_id = \""+ str(keyIssueEntry) + "\"")
                session.commit()
                keyIssueResultLabel["text"] = "Entry "+ str(keyIssueEntry) + " has been deleted."
            except Exception:
                keyIssueResultLabel["text"] = "Entry "+ str(keyIssueEntry) + " could not be deleted. Please check if it is in the table."
            cursor.close()
            session.close()

        def searchKeyIssue(self,keyIssueEntry):
            session = connect()
            cursor = session.cursor()

            try:
                #get that entry
                cursor.execute("SELECT * FROM issues WHERE issue_id = \""+ str(keyIssueEntry) + "\"")
                result = cursor.fetchall()
            
                for currentRow in result:
                    issue_id = currentRow[0]
                    issue_name = currentRow[1]
                    issue_description = currentRow[2]

                keyIssueResultLabel["text"] = keyIssueStringFormat(issue_id,issue_name,issue_description) + "."
            except Exception:
                keyIssueResultLabel["text"] = "Entry "+ str(keyIssueEntry) + " could not be found. Check if it was inserted into the table."
            cursor.close()
            session.close()

        def show10KeyIssue(self,start):
            session = connect()
            
            if start == '':
                start = 0

            cursor = session.cursor()
            cursor.execute("SELECT * FROM issues")
            result = cursor.fetchall()

            resultList = ""
            #get results x for x+y
            sliceResults = result[slice(int(start),int(start) + 10)]
            for currentRow in sliceResults: 
                    issue_id = currentRow[0]
                    issue_name = currentRow[1]
                    issue_description = currentRow[2]
                    
                    resultList += keyIssueStringFormat(issue_id,issue_name,issue_description) + "\n"
                    keyIssueResultLabel["text"] = resultList
            
            cursor.close()
            session.close()

        def updateKeyIssues(self,issuesEntry): 
            db_session = connect()
            cursor = db_session.cursor()

            splitString = str(issuesEntry).split(',')
            issue_id = splitString[0]
            issue_name = splitString[1]
            issue_description = splitString[2]

            try:
                cursor = db_session.cursor()   
                cursor.execute("SELECT * FROM issues WHERE issue_id = \""+ str(issue_id) + "\"")
                result = cursor.fetchall()
                for currentRow in result:
                    resultIssue_name = currentRow[1]
                    resultIssue_description = currentRow[2]

                if issue_name == '':
                    issue_name = resultIssue_name
                if issue_description == '':
                    issue_description = resultIssue_description

                cursor.execute("UPDATE issues SET issue_name =%s, issue_description = %s WHERE issue_id = \""+ issue_id + "\"",
                (issue_name, issue_description))
                db_session.commit()
                keyIssueResultLabel["text"] =  keyIssueStringFormat(issue_id,issue_name,issue_description)+" has been updated."
            except Exception:
                keyIssueResultLabel["text"] = "Entry "+ str(issue_id) + " could not be found. Check if it was inserted into the table."
            
            db_session.close()
            cursor.close()

        keyIssueFrameLabel = ttk.Label(self, text = "Issue Frame")
        keyIssueFrameLabel.grid(row = 1,column = 2)

        keyIssueAtrributeLabel = ttk.Label(self, text = "Values: issue_id, issue_name, issue_description "
                                                        +"\nExample: 0, Abortion, \"early\" child birth",
                                                         font = labelFont)
        keyIssueAtrributeLabel.grid(row = 1, column = 2)

        yearFrameButton = ttk.Button(self, text = "Year Frame", command = lambda: controller.show_frame(YearFrame))
        yearFrameButton.grid(row =1, column = 1)

        stateFrameButton = ttk.Button(self, text = "State Frame", command = lambda: controller.show_frame(StateFrame))
        stateFrameButton.grid(row =2, column = 1)

        debateFrameButton = ttk.Button(self, text = "Debate Frame", command = lambda: controller.show_frame(DebateFrame))
        debateFrameButton.grid(row =3, column = 1)

        conventionFrameButton = ttk.Button(self, text = "Convention Frame", command = lambda: controller.show_frame(ConventionFrame))
        conventionFrameButton.grid(row =4, column = 1)

        personFrameButton = ttk.Button(self, text = "Person Frame", command = lambda: controller.show_frame(PersonFrame))
        personFrameButton.grid(row =7, column = 1)
        
        stanceFrameButton = ttk.Button(self, text = "Stance Frame", command = lambda: controller.show_frame(StanceFrame))
        stanceFrameButton.grid(row =8, column = 1)

        mainFrameButton = ttk.Button(self, text = "Title", command = lambda: controller.show_frame(MainFrame))
        mainFrameButton.grid(row =9, column = 1)

        miscellaneousFrameButton = ttk.Button(self, text = "Miscellaneous Frame", command = lambda: controller.show_frame(MiscellaneousFrame))
        miscellaneousFrameButton.grid(row =10, column = 1)

        #entries
        keyIssueInsertEntry = tk.Entry(self, bg= 'white', width = 40)
        keyIssueInsertEntry.grid(row =3, column =2)

        keyIssueDeleteEntry = tk.Entry(self, bg = "white", width = 20)
        keyIssueDeleteEntry.grid(row = 3,column = 3)

        keyIssueSearchEntry = tk.Entry(self, bg = "white", width = 20)
        keyIssueSearchEntry.grid(row = 3, column = 4)

        keyIssueUpdateEntry = tk.Entry(self, bg= 'white', width = 60)
        keyIssueUpdateEntry.grid(row =3, column =5)

        keyIssue10SearchEntry = tk.Entry(self,bg = "white", width = 10)
        keyIssue10SearchEntry.grid(row = 3, column =6)

        #query buttons
        keyIssueInsertButton = ttk.Button(self, text = "insert",  command = lambda: insertKeyIssue(self,keyIssueInsertEntry.get()))
        keyIssueInsertButton.grid(row = 2, column =2)

        keyIssueDeleteButton = ttk.Button(self, text = "delete", command = lambda: deleteKeyIssue(self,keyIssueDeleteEntry.get()))
        keyIssueDeleteButton.grid(row = 2, column = 3)

        keyIssueSearchButton = ttk.Button(self, text = "search", command = lambda: searchKeyIssue(self,keyIssueSearchEntry.get()))
        keyIssueSearchButton.grid(row = 2, column = 4)

        keyIssueUpdateButton = ttk.Button(self, text = "update", command = lambda: updateKeyIssues(self,keyIssueUpdateEntry.get()))
        keyIssueUpdateButton.grid(row =2, column =5)

        keyIssue10SearchButton = ttk.Button(self, text = "10 Entries", command = lambda: show10KeyIssue(self,keyIssue10SearchEntry.get()))
        keyIssue10SearchButton.grid(row = 2, column =6)

        #display results
        keyIssueResultLabel = tk.Label(self, bg = "white", bd = 10, font = labelFont)
        keyIssueResultLabel.grid(row = 5, column = 2)


class MiscellaneousFrame(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        #functions
        #get the total amount of debates held over the years
        def getTotal(self,table):
            db_session = connect()
            cursor = db_session.cursor()

            if str(table).isupper:
                table = str(table).lower()  

            try:
                cursor.execute("SELECT COUNT(*) FROM " + str(table))
                totalCount = cursor.fetchone()[0] #get the 4 from [(4,)]
                miscellaneousResultLabel['text'] = "The total number of" + str(table) + " (s) entries in the database is " + str(totalCount) + "."
            except Exception:
                miscellaneousResultLabel['text'] = "Please enter an actual table name."

            cursor.close()
            db_session.close()

        def democratVSrepublican(self,table):
            #force input to be lower case
            if str(table).isupper:
                table = str(table).lower()
            
            #if these tables are passed in don't perform anything since these tables don't have a party attribute
            if table == "debate" or table == "issues" or table == "stance":
                miscellaneousResultLabel['text'] = "Cannot create a visual graph. Please enter elect_year, state, person, or convention."
                return None
            
            db_session = connect()
            cursor = db_session.cursor()

            #have arrays to hold the names and count of democrat,republican, and other
            partyNames = ["democrat","republican","other"]
            partyCount = [0,0,0]
            try:
                #Get the total number of entries in table
                cursor.execute("SELECT COUNT(*) FROM " + str(table))
                totalCount = cursor.fetchone()[0] #get the 4 from [(4,)]

                #set plot window size
                plt.figure(figsize=(10,5))

                #go through each entry and figure out if the party is democrat or republican
                cursor.execute("SELECT * FROM " + str(table))
                result = cursor.fetchall()
                for currentResult in result:
                    for currentResultIndex in currentResult:
                        currentResultIndex = str(currentResultIndex).lower()
                        if currentResultIndex == "democrat":
                            partyCount[0] += 1
                        elif currentResultIndex == "republican":
                            partyCount[1] += 1
                        
                #figure out how many others there are IE: not democrat or republican
                democratRepublicanSum = partyCount[0]+ partyCount[1]
                partyCount[2]= totalCount-democratRepublicanSum
                
                #show plot
                plt.bar(partyNames,partyCount)
                plt.ylabel("Total nmuber of enties in "+ str(table) + ".")
                plt.show()

                miscellaneousResultLabel['text'] = "The total number of" + str(table) + " (s) entries in the database is " + str(totalCount) + "."
            except Exception:
                miscellaneousResultLabel['text'] = "Cannot create a visual graph. Please enter elect_year, state, person, or convention."

            cursor.close()
            db_session.close()


        miscellaneousFrameLabel = ttk.Label(self, text = "Miscellaneous Frame", font = labelFont)
        miscellaneousFrameLabel.grid(row = 1,column = 2)

        tabelLabel = ttk.Label(self, text = "Tables: election_year, state, debate, convention, person, stance, issues", font = labelFont)
        tabelLabel.grid(row =1,column = 3, padx = 13)

        yearFrameButton = ttk.Button(self, text = "Year Frame", command = lambda: controller.show_frame(YearFrame))
        yearFrameButton.grid(row =1, column = 1)

        stateFrameButton = ttk.Button(self, text = "State Frame", command = lambda: controller.show_frame(StateFrame))
        stateFrameButton.grid(row =2, column = 1)

        debateFrameButton = ttk.Button(self, text = "Debate Frame", command = lambda: controller.show_frame(DebateFrame))
        debateFrameButton.grid(row =3, column = 1)

        conventionFrameButton = ttk.Button(self, text = "Convention Frame", command = lambda: controller.show_frame(ConventionFrame))
        conventionFrameButton.grid(row =4, column = 1)

        personFrameButton = ttk.Button(self, text = "Person Frame", command = lambda: controller.show_frame(PersonFrame))
        personFrameButton.grid(row =7, column = 1)
        
        stanceFrameButton = ttk.Button(self, text = "Stance Frame", command = lambda: controller.show_frame(StanceFrame))
        stanceFrameButton.grid(row =8, column = 1)

        keyIssueFrameButton = ttk.Button(self, text = "Issue Frame", command = lambda: controller.show_frame(KeyIssueFrame))
        keyIssueFrameButton.grid(row = 9, column = 1)

        mainFrameButton = ttk.Button(self, text = "Title", command = lambda: controller.show_frame(MainFrame))
        mainFrameButton.grid(row =10, column = 1)

        #all entries for buttons that need it
        countEntry = tk.Entry(self, bg = 'white', width = 10)
        countEntry.grid(row =3, column =2)

        graphEntry = tk.Entry(self, bg = 'white', width = 10)
        graphEntry.grid(row =3, column =3)

        #buttons that return a query
        countButton = ttk.Button(self, text = "count",  command = lambda: getTotal(self,countEntry.get()))
        countButton.grid(row = 2, column =2)

        graphButtion = ttk.Button(self, text = "graph", command = lambda:  democratVSrepublican(self,graphEntry.get()))
        graphButtion.grid(row = 2, column = 3)

        #display results
        miscellaneousResultLabel = tk.Label(self, bg = "white", bd = 10, font = labelFont)
        miscellaneousResultLabel.grid(row = 5, column = 2)


app = tkinterApp() 
app.mainloop() 