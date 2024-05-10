import fastf1
import fastf1.plotting
import numpy as np
import logging
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.collections import LineCollection
from matplotlib import cm
import seaborn as sns


def F1_info():
    # Enable cache
    fastf1.Cache.enable_cache('cache')
    
    # Set the logging level for the 'fastf1' package to 'WARNING' to limit the number of logged messages
    logging.getLogger('fastf1').setLevel(logging.WARNING)

    # The misc_mpl_mods option enables minor grid lines which clutter the plot
    fastf1.plotting.setup_mpl(misc_mpl_mods=False, color_scheme='None')

    years_availables = list(range(2018,2023))
    countries_availables = []
    circuits_availables = []
    drivers_dic = {}
    drivers_availables = []

    year = 2023
  
    schedule = fastf1.get_event_schedule(year)
    for i in range(len(schedule)):
        countries_availables.append(schedule['Country'][i])
        circuits_availables.append(schedule['Location'][i])

    def race_control():
        while True:
            race = str(input("Select a race. If you don't know the circuit's name or country write !countries or !circuits to see the corresponding list: \n")).title()

            if race not in countries_availables and race not in circuits_availables:
                if race == "!Countries":
                    print(countries_availables, "\n")
                elif race == "!Circuits":
                    print(circuits_availables, "\n")
                elif race == "!Exit":
                    exit()
                else:
                    print("The value entered is not the name of any circuit, country or command, please try again or type !exit to exit. \n")
            else:
                return race
            
    race = race_control()

    session = fastf1.get_session(year, race, 'R')
    session.load()

    race_info = session.results
    for i in range(len(race_info)):
        drivers_dic[race_info.iloc[i]['FullName']] = race_info.iloc[i]['Abbreviation']
        drivers_availables.append(race_info.iloc[i]['Abbreviation'])

    def driver_control():
        while True:
            driver = str(input('Choose a driver by his abbreviation, type !drivers to get a list of the drivers availables or !exit to exit: \n')).upper()
            if driver not in drivers_availables:
                if driver == "!DRIVERS":
                    print(drivers_availables, "\n")
                elif driver == "!EXIT":
                    exit()
                else:
                    print("Something went wrong, please try again")
            else:
                return driver
    
    driver1 = driver_control()

    driver2 = driver_control()
 
    drivers = [driver1, driver2]

    # 1. Position changes during a race
    fig, ax = plt.subplots(figsize=(12,6))
    fig.suptitle(f'Position Evolution', size=24, y=0.99)

    for drv in drivers:
        drv_laps = session.laps.pick_driver(drv)

        abb = drv_laps['Driver'].iloc[0]
        color = fastf1.plotting.driver_color(abb)   
        
        ax.plot(drv_laps['LapNumber'], drv_laps['Position'],
                label=abb, color=color)
        
    ax.set_ylim([20.5, 0.5])
    ax.set_yticks([1, 5, 10, 15, 20])
    ax.set_xlabel('Lap')
    ax.set_ylabel('Position')    

    ax.legend(bbox_to_anchor=(1.0, 1.02))
    plt.tight_layout()
    plt.show()

    # 2. Overlaying speed traces of two laps
    fig, ax = plt.subplots(figsize=(12,6))
    fig.suptitle(f'Fastest Lap', size=24, y=0.98)

    for drv in drivers:
        driver_lap = session.laps.pick_driver(drv).pick_fastest()
        driver_tel = driver_lap.get_car_data().add_distance()
        driver_color = fastf1.plotting.driver_color(drv)
        ax.plot(driver_tel['Distance'], driver_tel['Speed'], color= driver_color, label= drv)

    ax.set_xlabel('Distance in m')
    ax.set_ylabel('Speed in km/h')
    ax.legend()
    
    plt.show()

    # 3. Gear shifts on track
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))    

    for i, driver in enumerate(drivers):
        lap = session.laps.pick_driver(driver).pick_fastest()
        tel = lap.get_telemetry()

        x = np.array(tel['X'].values)
        y = np.array(tel['Y'].values)
        
        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        gear = tel['nGear'].to_numpy().astype(float)
        cmap = cm.get_cmap('Paired')
        lc_comp = LineCollection(segments, norm=plt.Normalize(1, cmap.N+1), cmap=cmap)
        lc_comp.set_array(gear)
        lc_comp.set_linewidth(4)
        
        axes[i].add_collection(lc_comp)
        axes[i].axis('equal')
        axes[i].tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)

        fig.suptitle(
            f"Fastest Lap Gear Shift Visualization", size=24, y=0.99)
        axes[i].set_title(f"{driver}")

        cbar = fig.colorbar(mappable=lc_comp, ax=axes[i], label="Gear",
                        boundaries=np.arange(1, 10))
        cbar.set_ticks(np.arange(1.5, 9.5))
        cbar.set_ticklabels(np.arange(1, 9))

    plt.show()

    # 4. Tyre strategies during a race
    laps = session.laps

    stints = laps[["Driver", "Stint", "Compound", "LapNumber"]]
    stints = stints.groupby(["Driver", "Stint", "Compound"])
    stints = stints.count().reset_index()

    stints = stints.rename(columns={"LapNumber": "StintLength"})
    
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.suptitle(f'Tyre Strategies', size=24, y=0.98)

    for driver in drivers:
        driver_stints = stints.loc[stints["Driver"] == driver]

        previous_stint_end = 0
        for idx, row in driver_stints.iterrows():
            # each row contains the compound name and stint length
            # we can use these information to draw horizontal bars
            plt.barh(
                y=driver,
                width=row["StintLength"],
                left=previous_stint_end,
                color=fastf1.plotting.COMPOUND_COLORS[row["Compound"]],
                edgecolor="black",
                fill=True
            )

            previous_stint_end += row["StintLength"]

    plt.xlabel("Lap Number")
    plt.grid(False)
    # invert the y-axis so drivers that finish higher are closer to the top
    ax.invert_yaxis()

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.tight_layout()
    plt.show()
    

    # 5. Speed visualization on track map
    colormap = mpl.cm.plasma

    # We create a plot with title and adjust some setting to make it look good.
    fig, axs = plt.subplots(1, 2, sharex=True, sharey=True, figsize=(14, 8))
    fig.suptitle(f'Fastest Lap Speed Visualization', size=24, y=0.99)

    for i, driver in enumerate(drivers):
        lap = session.laps.pick_driver(driver).pick_fastest()

        # Get telemetry data
        x = lap.telemetry['X']              # values for x-axis
        y = lap.telemetry['Y']              # values for y-axis
        color = lap.telemetry['Speed']      # value to base color gradient on

        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        # Adjust margins and turn off axis
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
        axs[i].axis('off')

        # After this, we plot the data itself.
        # Create background track line
        axs[i].plot(lap.telemetry['X'], lap.telemetry['Y'],
                    color='black', linestyle='-', linewidth=16, zorder=0)

        # Create a continuous norm to map from data points to colors
        norm = plt.Normalize(color.min(), color.max())
        lc = LineCollection(segments, cmap=colormap, norm=norm, 
                            linestyle='-', linewidth=5)

        # Set the values used for colormapping
        lc.set_array(color)

        # Merge all line segments together
        axs[i].add_collection(lc)

        # Add title with driver's name
        axs[i].set_title(driver, fontsize=16)

    # Finally, we create a color bar as a legend.
    cbaxes = fig.add_axes([0.1, 0.05, 0.8, 0.05])
    normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
    legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap, 
                                       orientation="horizontal")
    
    # Show the plot
    plt.show()


F1_info()