import * as React from 'react';
import Paper from '@mui/material/Paper';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import {EditingState, IntegratedEditing, ViewState} from '@devexpress/dx-react-scheduler';
import {
    AppointmentForm,
    Appointments,
    AppointmentTooltip,
    ConfirmationDialog,
    DateNavigator,
    DayView,
    MonthView,
    Resources,
    Scheduler,
    TodayButton,
    Toolbar,
    WeekView,
    AllDayPanel
} from '@devexpress/dx-react-scheduler-material-ui';


import {get,post} from '../utils/requests'


import { eventLabels } from './Globals.js';

import Button from "@mui/material/Button";
import EventAvailableOutlinedIcon from '@mui/icons-material/EventAvailableOutlined';
import CustomAppointmentForm from "./CustomAppointmentForm";
import {useRef} from "react";


const CustomButton = ({invite_email,event_id,onClick}) => {



    const onExecute = () => {
        if(invite_email===""||invite_email===null){
            alert("input_email")
        }else{
            const param = {email:invite_email,event_id:event_id}
            post("/api/event/invite/",param)
                .then(function (res){
					if(res.status === 200){
						alert("Invitation sent successfully!");
						onClick()
					}else if(res.status === 401){
						alert("Guest is already invited!");
                    }else{
						alert("Invitation failed to send, plese check the email address!");
					}
                }).catch(function (res){
					  alert("Invitation failed to send, plese try another email address!");

				  })
        }
    }
    return (
        <Button variant="contained" color="primary" onClick={onExecute}>Invite</Button>
    );
};

const BasicLayout = ({ onFieldChange, appointmentData, ...restProps }) => {

  const [invite_email,setInviteEmail] = React.useState("");
    const [signal, setSignal] = React.useState(false);

 return (
  <AppointmentForm.BasicLayout
    appointmentData={appointmentData}
    onFieldChange={onFieldChange}
    {...restProps}
	>

      {appointmentData.id?
          (<div style={{ display: 'flex', alignItems: 'center' }}>
                  <AppointmentForm.TextEditor
                      value={invite_email}
                      onValueChange={(value)=>setInviteEmail(value)}
                      placeholder="Enter an email address"
                      readOnly={false}
                      style={{ marginRight: '16px' }} // add some margin between the editor and button
                        type={"email"}/>
                  <AppointmentForm.CommandButton command="Invite +" />
                  <CustomButton command="customAction" invite_email={invite_email} event_id={appointmentData.id} onClick={()=>{setSignal(true)}}  />
              </div>):(<div></div>)}
      {appointmentData.id?
          (<CustomAppointmentForm event_id={appointmentData.id} signal={signal}  />):(<div></div>)}
    </AppointmentForm.BasicLayout>
);
};


const ExternalViewSwitcher = ({currentViewName, onChange, }) => 
	
(<RadioGroup
    aria-label="Views"
    style={{ flexDirection: 'row' }}
    name="views"
    value={currentViewName}
    onChange={onChange}
  >
  
  	{/* <--- Radio buttons --->  */}

    <FormControlLabel value="Day" control={<Radio />} label="Day" />
    <FormControlLabel value="Week" control={<Radio />} label="Week" />
    <FormControlLabel value="Month" control={<Radio />} label="Month" />

	
  </RadioGroup>
);



export default class Schedule extends React.PureComponent {
  constructor(props) {
    super(props);


	/* State variable to keep track of appointment form visibility */

    this.state = {
        data: [],
        realData : [],
        addNewEvent: false,
        mainResourceName: 'Label',
        currentViewName: 'Month' ,
        resources: [
        /* <--- This displays the label field and drop down selection--->  */
            {
                fieldName: "label_id",
                title: "Label",
                instances: [],
            }
        ],
    };


	
    this.currentViewNameChange = (e) => {
      this.setState({ currentViewName: e.target.value });

    };
	this.currentDateChange = (currentDate) => { this.setState({ currentDate }); };
    this.commitChanges = this.commitChanges.bind(this);

	/* Method to toggle appointment form visibility */

    this.showAppointmentForm = (bool) => {
	
         this.setState({addNewEvent: bool})
	
    };


  }
  

    componentDidUpdate(prevProps,prevStates) {

      const {label_id,label_data} = this.props
        const {data} = this.state

        if(data !== prevStates.data){
            let newData = []
            data.forEach(value=>{
                if(value['label_id']===label_id){
                    newData.push(value)
                }
            })
            this.setState({realData: newData})
        }


        if (label_id !== prevProps.label_id) {
            let that = this
            this.getEventList(label_id)
                .then(function (res){
                    that.setState({data:res})
                })
        }

        // format and add label_data for user choosing
        if(label_data !== prevProps.label_data){
            let {resources} = this.state
            let label = resources[0];
            label.instances = [];
            label_data.forEach(value=>{
                value['text'] = value['name']
                delete value['name']
                delete value['owner']
                label.instances.push(value)
            })
            this.setState({resources:[label]})
        }

    }

    async getEventList(label_id) {
        let dataVal = [];
        await get("/api/event/get_list", {"id": label_id})
            .then(function (res) {
                let data = res.data
                data.forEach(value => {
                    value['startDate'] = new Date((value['startTime']))
                    value['endDate'] = new Date(value['endTime'])
                    value['label_id'] = value['labelId']

                    delete value['startTime'];
                    delete value['endTime'];
                    delete value['labelId']
                    dataVal.push(value)
                })
            })
        return dataVal
    }
    
  	/* <--- Appointment editing and saving --->  */
   

    commitChanges({ added, changed, deleted }) {
	
			let {data} = this.state;


			if(added){
				if(added['label_id']=== undefined)
				{
					alert("Please select a label !");
					return;
				}
				
				if(added['title'] === undefined)
				{
					alert("Please fill title !");
					return;
				}

				let that = this
				data = [...data, { ...added }];
				let pos = data.length;
				added['startDate'] = Date.parse(added['startDate']);
				added['endDate'] = Date.parse(added['endDate']);


                if (added['startDate'] >= added['endDate']){
                    alert("Start time must be before end time")
                    return
                }


				/*if(added['allDay']===true)
					{
						var startDatee= new Date(added['startDate']);
						startDatee.setHours('08','00','00');
						added['startDate']=Date.parse(startDatee);
						
						var endDatee= new Date(added['endDate']);
						endDatee.setHours('18','00','00');
						added['endDate']=Date.parse(endDatee);
						added['allDay']=false;
						
					}*/
				
				post("/api/event/create/",added).then(
					function (res){
						let {data} = that.state
						data[pos-1].id = res.data
						that.setState({data:data})
					}
				)
			}
			if(changed){
				let newData =[]
				data.forEach(appointment=>{
					if(changed[appointment.id]){
						let c = { ...appointment, ...changed[appointment.id] }
						c['startDate'] = Date.parse(c['startDate']);
						c['endDate'] = Date.parse(c['endDate']);
                        if (c['startDate'] >= c['endDate']){
                            alert("Start time must be before end time")
                            newData.push(appointment)
                            return
                        }
						/*if(c['allDay']===true)
						{
							var startDatee= new Date(c['startDate']);
							startDatee.setHours('08','00','00');
							c['startDate']=Date.parse(startDatee);
							
							var endDatee= new Date(c['endDate']);
							endDatee.setHours('18','00','00');
							c['endDate']=Date.parse(endDatee);
							c['allDay']=false;
							
						}*/
						
						post("/api/event/update/",c)
							.then(function (res){
								console.log(res)
							})
						newData.push({ ...appointment, ...changed[appointment.id] })
					}else{
						newData.push(appointment)
					}
				})
				data = newData
			}
			if(deleted){
				data = data.filter(appointment => appointment.id !== deleted);
				post("/api/event/delete/", {"event_id": deleted}).then(res=>{console.log(res)})
			}


			this.setState({data:data})
			this.setState({addNewEvent:false})

    }
  
  

  render() {

    const { realData, data, currentViewName, currentDate, resources } = this.state;
	

    return (

      <React.Fragment>
        <ExternalViewSwitcher
          currentViewName={currentViewName}
          onChange={this.currentViewNameChange}
        />
        <Paper>
            <Scheduler data={realData} height={570}>
            <ViewState
              defaultCurrentDate={new Date()}
              currentViewName={currentViewName}
              onCurrentDateChange={this.currentDateChange}
            />
			{/* <--- Appointment editing --->  */}
            <EditingState onCommitChanges={this.commitChanges} />
            <IntegratedEditing />


            {/* <--- Daily view --->  */}
            <DayView startDayHour={0} endDayHour={24}/>
		  
            {/* <--- Weekly view --->  */}
            <WeekView startDayHour={0} endDayHour={24}/>
          		 
            {/* <--- Monthly view --->  */}
            <MonthView />

			 <Button 
				variant="contained" 
				sx={{maxWidth: '200px', maxHeight: '40px', float:'right'}} 
				color="primary" 
				startIcon={<EventAvailableOutlinedIcon />}
				onClick={this.showAppointmentForm.bind(null,true)} >
			 Add new event
			 </Button>


            {/* <--- Appointment form popup for creation and edit --->  */}
            <Appointments/>
                <AllDayPanel/>

            <AppointmentTooltip showOpenButton showDeleteButton/>
            <ConfirmationDialog />

            <Toolbar />
            <DateNavigator />
            <TodayButton />

			<AppointmentForm visible={this.state.addNewEvent} 
				onVisibilityChange={this.showAppointmentForm.bind(null)}
				basicLayoutComponent={BasicLayout} />
            <Resources
                data={resources}
                mainResourceName="label_id"
            />

            </Scheduler>
        </Paper>
      </React.Fragment>
    );
  }
}
