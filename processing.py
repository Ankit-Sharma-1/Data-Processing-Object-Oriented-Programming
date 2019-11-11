"""
    Logical processing classes used in the second assignment for CSSE1001/7030.

    ProcessResults: Abstract class that defines the logical processing interface.
    AthleteResults: Provides details of one athlete’s results for all of the
                    events in which they competed.
    CountryResults: Provides a summary of the results of all athletes who
                    competed for one country.
    EventResults  : Provides details of the results of all athlete's who
                    competed in one event.
    DeterminePlaces: Determines the place ranking of all athletes who competed
                     in one event.
"""

__author__ = "Ankit Sharma"
__email__ = "ankit.sharma@uqconnect.edu.au"



from entities import Athlete, Result, Event, Country, ManagedDictionary
from entities import all_athletes, all_countries, all_events, load_data

from operator import itemgetter


class ProcessResults(object) :
    """Superclass for the logical processing commands."""

    _processing_counter = 0  # Number of times any process command has executed.
    
    def process(self) :
        """Abstract method representing collecting and processing results data.
        """
        ProcessResults._processing_counter += 1
    
    def get_results(self) :
        """Abstract method representing obtaining the processed results.

        Return:
            list: Subclasses will determine the contents of the resulting list.
        """
        raise NotImplementedError()



class AthleteResults(ProcessResults) :
    """Determines the results achieved by one athlete."""

    _athlete_results_counter = 0  # Number of times this command has executed.

    def __init__(self, athlete) :
        """
        Parameters:
            athlete (Athlete): Athlete for whom we wish to determine their results.
        """
        self._athlete = athlete
        self._results = []
        self._place = []

    def process(self) :
        """Obtain all the results for this athlete and
           order them from best to worst placing.
           If two or more results have the same place they should be ordered
           by event name in ascending alphabetical order.
        """
        super().process()
        AthleteResults._athlete_results_counter += 1
        
        for event in self._athlete.get_events():
            self._place.append((int(self._athlete.get_result(event).get_place()),
                               event.get_name(),self._athlete.get_result(event)))

        
        for place in sorted(self._place):
            self._results.append(place[2])

    def get_results(self) :
        """Obtain the processed results for _athlete.

        Return:
            list[Result]: Ordered list of the _athlete's results.
                          Sorted from best to worst, based on place in event.
                          Results with the same place are ordered by event name
                          in ascending alphabetical order.

        Raises:
            ValueError: If process has not yet been executed.
        """
        if self._results == []:
            raise ValueError("Process has not yet been executed")  
        else:
            return self._results

    def get_usage_ratio() :
        """Ratio of usage of the AthleteResults command against all commands.

        Return:
            float: ratio of _athlete_results_counter by _processing_counter.
        """
        return (AthleteResults._athlete_results_counter
                / AthleteResults._processing_counter)

    def __str__(self) :
        """(str) Return a formatted string of the results for this athlete."""
        """Implementation of this is optional but useful for observing your
           programs behaviour.
        """
        return self._athlete 

class DeterminePlaces(ProcessResults) :
    """Determines the results achieved by one athlete."""

    _determine_places_counter = 0  # Number of times this command has executed.

    def __init__(self, event) : #Takes Event object on which processing occurs
        """
        Parameters:
            athlete (Athlete): Athlete for whom we wish to determine their results.
        """
        self._event = event
        self._athletes = []
        self._results = []
        self._athlete = []

 
    def process(self) :
        """Obtain all the results for the event and
           order them from best to worst placing.
           If two or more results have the same place they should be ordered
           by event name in ascending alphabetical order.
        """
        super().process()
        DeterminePlaces._determine_places_counter += 1

        """
        #Get athlete id, result and fullname for all atheletes participating in an event
        for athlete in self._event.get_athletes():
            result_value = float(athlete.get_result(self._event).get_result())
            print(result_value)
            self._results.append((result_value,athlete.get_full_name(),athlete))
                
        #Based on event being timed or not results are ordered
        if self._event.is_timed():
            self._final_place = sorted(self._results)
        else:
            self._final_place = sorted(self._results, reverse = True)
                   
        #Take athlete ids from sorted result
        for result in self._final_place:
            self._athlete_places.append(result[2])
        """
        self._athletes = self._event.get_athletes()

        if self._event.is_timed():
            results = {}
            for athlete in self._athletes:
                result = athlete.get_result(self._event)
                results[athlete] = result
            
            results_list = results.items()
            #Sorting by results and athlete name
            results_sorted = sorted(results_list, key = lambda z : (float(z[1].get_result()), str(z[0].get_full_name())))
            self._results = [x[0] for x in results_sorted]

        else:
            results = {}
            for athlete in self._athletes:
                result = athlete.get_result(self._event)
                results[athlete] = result
            
            results_list = results.items()
            #Sorting by results and athlete name
            results_sorted = sorted(results_list, key = lambda z : (float(z[1].get_result()), str(z[0].get_full_name())))
            self._results = [x[0] for x in results_sorted]
                
        #Assigning a place athletes based on ordered results for the event:
        "If there is a tie, the place following the tie skips by the number of tied athletes"
        pos = 1
        tied_athlete_count = 0
        
        for position in results_sorted:
            self._athlete = position[0]
            if tied_athlete_count == 0:
                self._athlete.get_result(self._event).set_place(pos)
                pos += 1
                pos += tied_athlete_count
                tied_athlete_count = 0
            else:
                self._athlete.get_result(self._event).set_place(pos)
                tied_athlete_count += 1

    def get_results(self) :
        """Obtain the processed results for _event.

        Return:
            list[Athlete object]:Ordered list of Athlete objects
                                 Based on logic implemented in the process method

        Raises:
            ValueError: If process has not yet been executed.
        """
        if self._results != []:
            print(self._results)
        else:
            raise ValueError ('Process has not yet been executed')


    def get_usage_ratio() :
        """Ratio of usage of the DeterminePlaces command against all commands.

        Return:
            float: ratio of _determine_places_counter by _processing_counter.
        """
        return (DeterminePlaces._determine_places_counter
                / DeterminePlaces._processing_counter)

    def __str__(self) :
        """(str) Return a formatted string of the athlete objects
                 ordered by position for this event."""
        return self._athlete_places
    
    def __repr_(self):
        return str(self)

class EventResults(ProcessResults):
    """Obtaining results of all athletes competing in one event"""
    
    _event_results_counter = 0  # Number of times this command has executed.

    def __init__(self, event) :
        """
        Parameters:
            athlete (Athlete): Athlete for whom we wish to determine their results.
        """
        self._event = event
        self._results = []
        self._athletes = []

    def process(self) :
        """Obtain all athletes for this event
        """
        super().process()
        EventResults._event_results_counter += 1
        self._athletes = self._event.get_athletes()

        results = {}
        for athlete in self._athletes:
            result = athlete.get_result(self._event)
            results[athlete] = result

        #Sort results by places and athlete name
        results_list = results.items()
        results_sorted = sorted(results_list, key = lambda z : (int(z[1].get_place()), str(z[0].get_full_name())))
        self._results = [x[0] for x in results_sorted]

    def get_results(self) :
        """Obtain the processed results for _event.

        Return:
            list[Athlete]: Ordered list of the _event's athletes.
                          ordered by athlete name in ascending alphabetical
                          order.

        Raises:
            ValueError: If process has not yet been executed.
        """
        if self._results != []:
            print(self._results)
        else:
            raise ValueError ('Process has not yet been executed')

    def get_usage_ratio() :
        """Ratio of usage of the AthleteResults command against all commands.

        Return:
            float: ratio of _athlete_results_counter by _processing_counter.
        """
        return (EventResults._event_results_counter
                / EventResults._processing_counter)

    def __str__(self) :
        """(str) Return a formatted string of the athlete objects for this event."""
        return self._athletes

class CountryResults(ProcessResults):
    """obtain a summary of the results of one country’s delegation"""

    _country_results_counter = 0  # Number of times this command has executed.
    
    def __init__(self,country):
        self._country = country
        self._gold = 0
        self._silver = 0
        self._bronze = 0
        self._athlete = []
        self._results = []

    def process(self):
        """
            Determine how many gold, silver and bronze medals were won by athletes who
            competed for the country.
        """
        super().process()
        CountryResults._country_results_counter += 1

        
        # Add medal count based on athlete perforamnce
        for athlete in self._country.get_athletes():
            for event in athlete.get_events():
                if athlete.get_result(event).get_medal()=='Gold':
                    self._gold += 1
                elif athlete.get_result(event).get_medal()=='Silver':
                    self._silver += 1
                elif athlete.get_result(event).get_medal()=='Bronze':
                    self._bronze += 1
                else:
                    pass

        #Storing result in self._results
        gold = self._gold
        silver = self._silver
        bronze = self._bronze
        
        self._results = [gold,silver,bronze, len(self._country.get_athletes())]
        
    def get_results(self):
        if self._results != []:
            return self._results
        else:
            raise ValueError('Process has not been done')
        
    def get_num_gold(self):
        """return number of gold medals won by a country"""
        return self._gold
    
    def get_num_silver(self):
        """return number of silver medals won by a country"""
        return self._silver
    
    def get_num_bronze(self):
        """return number of bronze medals won by a country"""
        return self._bronze
    
    def get_num_athletes(self):
        """return number of athletes competing for th country"""
        return len(self._country.get_athletes())
    
    def get_usage_ratio():
        """Ratio of usage of the CountryResults command against all commands.

        Return:
            float: ratio of _country_results_counter by _processing_counter.
        """
        return (CountryResults._country_results_counter
                / CountryResults._processing_counter)

    def __str__(self):
        """(str) Return a formatted string of the medal counts and total athletes for this country."""
        return self._results
