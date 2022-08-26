import streamlit as st
import pandas as pd
import pickle
import sklearn

def predict (d_dep, d_arr, t_dep, t_arr, src, dst, airline, stops):

    if src == dst:
        st.error("Invalid Source and Destination choice")
        return None
    

    Journey_day = int(pd.to_datetime(d_dep, format="%Y-%m-%d").day)
    Journey_month = int(pd.to_datetime(d_dep, format ="%Y-%m-%d").month)


    Dep_hour = int(pd.to_datetime(t_dep, format ="%H:%M:%S").hour)
    Dep_min = int(pd.to_datetime(t_dep, format ="%H:%M:%S").minute)

    Arrival_hour = int(pd.to_datetime(t_arr, format ="%H:%M:%S").hour)
    Arrival_min = int(pd.to_datetime(t_arr, format ="%H:%M:%S").minute)

    dur_hour = abs(Arrival_hour - Dep_hour)
    dur_min = abs(Arrival_min - Dep_min)

    Total_stops = int(stops)

    airline = airline.replace(' ', '_')
    airlines = {
                "Jet_Airways": 0,
                "IndiGo": 0,
                "Air_India": 0,
                "Multiple_carriers": 0,
                "SpiceJet": 0,
                "Vistara": 0,
                "GoAir" :0,
                "Multiple_carriers_Premium_economy": 0,
                "Jet_Airways_Business": 0,
                "Vistara_Premium_economy": 0,
                "Trujet": 0
            }
    airlines[airline] = 1

    srcs =  {
                "Kolkata": 0,
                "Chennai": 0,
                "Bangalore": 0,
                "Delhi": 0,
                "Mumbai": 0
            }
    srcs[src] = 1

    dests = {
                "Kolkata": 0,
                "Hyderabad": 0,
                "New_Delhi": 0,
                "Delhi": 0,
                "Bangalore": 0,
                "Cochin": 0
            }
    dests[dst] = 1

    prediction = model.predict([[
        stops,
        Journey_day,
        Journey_month,
        Dep_hour,
        Dep_min,
        Arrival_hour,
        Arrival_min,
        dur_hour,
        dur_min,
        airlines['Air_India'],
        airlines['GoAir'],
        airlines['IndiGo'],
        airlines['Jet_Airways'],
        airlines['Jet_Airways_Business'],
        airlines['Multiple_carriers'],
        airlines['Multiple_carriers_Premium_economy'],
        airlines['SpiceJet'],
        airlines['Trujet'],
        airlines['Vistara'],
        airlines['Vistara_Premium_economy'],
        srcs['Chennai'],
        srcs['Delhi'],
        srcs['Kolkata'],
        srcs['Mumbai'],
        dests['Cochin'],
        dests['Delhi'],
        dests['Hyderabad'],
        dests['Kolkata'],
        dests['New_Delhi']
    ]])
    return prediction
    


def main():
    st.header("Know Your Fare")



    with st.form("MadeWithLove"):
        col1, col2 = st.columns(2)

        with col1:
            d_dep = st.date_input('Choose Departure Date: ')
            t_dep = st.time_input('Choose Departure Time: ')
            choice_src=st.selectbox(label="Choose Source",options=["Kolkata","Chennai","Bangalore","Delhi","Mumbai"])
            choice_airl=st.selectbox(label="Choose Airline",options=["Jet Airways","Indigo","Air India","Multiple carriers","SpiceJet","Vistara", "Air Asia", "GoAir",  "Multiple carriers Premium economy", "Jet Airways Business", "Vistara Premium economy", "Trujet"])

        with col2:
            d_arr = st.date_input('Choose Arrival Date: ')
            t_arr = st.time_input('Choose Arrival Time: ')
            choice_dest=st.selectbox(label="Choose Destination",options=["Kolkata","Hyderabad","New Delhi","Delhi","Bangalore","Cochin"])
            choice_stops=st.selectbox(label="Choose Number of Stops",options=["0","1","2","3","4"])
        

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted :
            fare = predict(d_dep, d_arr, t_dep, t_arr, choice_src, choice_dest, choice_airl, choice_stops)
            if fare is not None:
                st.success(f"Predicted Fare: INR. {fare[0]:.2f}")

if __name__ == "__main__":
    model = pickle.load(open("flight_rf.pkl", "rb"))
    main()


