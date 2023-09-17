import * as React from 'react';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import ListSubheader from '@mui/material/ListSubheader';

import CakeIcon from '@mui/icons-material/Cake';
import GroupsIcon from '@mui/icons-material/Groups';
import NotificationsActiveIcon from '@mui/icons-material/NotificationsActive';
import ListAltIcon from '@mui/icons-material/ListAlt';
import ModeOfTravelIcon from '@mui/icons-material/ModeOfTravel';

export const mainListItems = (
  <React.Fragment>
    <ListItemButton>
	  <ListItemIcon>
        <CakeIcon />
      </ListItemIcon>
      <ListItemText primary="Birthdays" />
    </ListItemButton>
    <ListItemButton>
	 <ListItemIcon>
        <GroupsIcon />
      </ListItemIcon>
      <ListItemText primary="Meetings" />
    </ListItemButton>
	<ListItemButton>
	 <ListItemIcon>
        <NotificationsActiveIcon />
      </ListItemIcon>
      <ListItemText primary="Reminders" />
    </ListItemButton>
	<ListItemButton>
	 <ListItemIcon>
        <ListAltIcon />
      </ListItemIcon>
      <ListItemText primary="Tasks" />
    </ListItemButton>
	<ListItemButton>
	 <ListItemIcon>
        <ModeOfTravelIcon />
      </ListItemIcon>
      <ListItemText primary="Travel" />
    </ListItemButton>
  </React.Fragment>
);