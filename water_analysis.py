import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import copy as cp
plt.style.use('fivethirtyeight')
sns.set_context(font_scale= 4)
class Data:     
     
    '''
    ##################      This is a analysis on water resources       #####################
    And this module can be used by passing 'water analysis file' as a parameter to the Data class.
    These are the available methods and fields to use:
    Field -> data
    
    Functions name:
    *     mimic_surge_error
    *     waterAmount_150_above
    *     waterAmount_150_less
    *     waterAmount_0_values
    *     fill_waterAmount_of_0_values
    *     leaky_taps
    *     rename_tap
    *     sort_filter_name
    *     visualizing_amount
    *     leakage_amount
    *     taps
    *     taps_location
    *     all_taps_location_plot
   
    '''
    __all__= {
    "mimic_surge_error",
    "waterAmount_150_above",
    "waterAmount_150_less",
    "waterAmount_0_values",
    "leaky_taps",
    "rename_tap",
    "sort_filter_name",
    "visualizing_amount",
    "leakage_amount",
    "taps",
    "taps_location",
    "all_taps_location_plot"
    ""
}    
    def __init__(self, df):
        self.data= cp.deepcopy(df)
    
    def rename_column_name(self, names):
        """
        Renaming the columns name to what is specified in the Data class
        
        """
        self.data.columns= names
    
    def mimic_surge_error(self):
        """
        The will return a dataframe that is less or equal to the specify surge value
        
        """
        surge = int(input("Specify surge value: "))
        return self.data[self.data['Amount_water'] <= surge] 
    
    def waterAmount_150_above(self):
        """
        This will return a dataframe, where the amount of water is greater than or equal to 150ml and less than 500ml
        
        """
        amount150=  self.data.loc[self.data["Amount_water"] >=150]
        amount500less = amount150[amount150["Amount_water"] < 500]
        return amount500less
    
    def waterAmount_150_less(self):
        amount150less= self.data[self.data["Amount_water"] < 150]
        return amount150less
    
    def waterAmount_0_values(self):
        """
        Returning a dataframe, where the amount of water is equal to zero values
        
        """
        zer= self.data['Amount_water']==0
        return self.data[zer]
    
    def fill_waterAmount_of_0_values(self):
        """
        This will replace all the instance of water amount of zero value with the mean of the column
        
        """
        self.data['Amount_water']= self.data['Amount_water'].replace(0, self.data['Amount_water'].mean())
        return self.data
    
    def leaky_taps(self):
        """
        Returning names of the leaky taps
        
        """
        leak= self.waterAmount_0_values()
        return leak.Filter_name
    
    def taps(self):
        """
        This method is only going to group all the taps into a list and then return the list.
        The return type is list, which you can slice or iterate through.
        
        """ 
        tap= []
        unique_tap= sorted(self.data['Filter_name'].unique())
        tap_length= len(unique_tap)
        for i in range(1, tap_length+1):
            tap.append(self.data[self.data['Filter_name'] == 'Tap '+ str(i)])
        return tap
    
    def taps_location(self):
        """
        This method is for grouping each tap according to their location into a list.
        The return type is list, which you can slice or iterate.
        
        """
        location=list(self.data['Filter_location'].unique())
        loc_num= len(location) #Length of Location number
        tap= self.taps()
        tap_location= [[], [], [], [], [], [], []]
        basetap= 0
        while basetap < 7:
            k= 0
            while k < loc_num:
                for j in location:
                    tap_loc = tap[basetap]
                    tap_location[k].append(tap_loc[tap_loc['Filter_location'] == j])
                    k += 1
            basetap += 1
        return tap_location #The slicing index can be change to 6 when the location is up to 6
    
    def all_taps_location_plot(self):    
        """
        This is method is going to return visualization for each tap and location.
        It then going to save it in a directory call "the location name" in taporder folder.
        
        """
        tapsL= self.taps_location() # Tap for different location
        try:
            for tap_loc in tapsL:
                location= tap_loc[0]['Filter_location'][0]                
                for j in range(0, 7):
                    plt.figure(figsize= (25, 13))
                    plt.plot(tap_loc[j].sort_index(ascending= True).index.values, tap_loc[j]['Amount_water'])
                    plt.ylabel('Amount of water', fontsize= 19)                
                    plt.title(f"Tap {j+1} for {location}", fontsize= 19)
                    plt.xticks(fontsize= 15)
                    plt.yticks(fontsize= 15)
                    plt.ylim([0, 903])
                    plt.xlabel('Time', fontsize= 19)
                    #plt.savefig('taporder/%s/tap %s.png' % (location, str(j + 1))) #To save visuals in taporder folder
        except IndexError:
            print("Nothing to display here")
    
    def rename_tap(self, name):
        self.data["Filter_name"].replace(name, inplace= True)
        
    def sort_filter_name(self):
        self.data.sort_values(by= "Filter_name", axis = 0, inplace= True)
        
    def _annot(self, splot, decide= True):
        for p in splot.patches:
            if decide:
                rounder= '.1f'
            else:
                rounder= '1d'
            splot.annotate(format(p.get_height(), rounder),\
                   (p.get_x() + p.get_width() / 2., p.get_height()),\
                   ha = 'center', va = 'center',\
                   size=15,\
                   xytext = (0, -12),\
                   textcoords = 'offset points')

    def visualizing_amount_bar(self, df):
        splot= sns.barplot(data= df.sort_values(by= 'Filter_name'), x= 'Filter_name', y= 'Amount_water', errcolor= 'none', palette= 'coolwarm')
        self._annot(splot)
            
    def visualizing_amount_location(self, df):
        splot= sns.barplot(data= df, x= 'Filter_location', y= 'Amount_water', errcolor= 'none', palette= 'coolwarm')
        plt.xticks(rotation= 40)
        self._annot(splot)
        
    def visualizing_location_count(self, df):
        if(isinstance(df, pd.DataFrame)):
            splot= sns.countplot(data= df, x= 'Filter_name', palette= 'coolwarm')
            self._annot(splot, decide= False)
        elif(isinstance(df, pd.Series)):
            splot=  sns.countplot(x= df, palette= 'coolwarm')
            self._annot(splot, decide= False)
    