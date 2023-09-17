import React, { useState } from 'react';
import { SketchPicker } from 'react-color';
import { TextField, Button, Popover } from '@mui/material';

const ColorPicker = ({ color , onColorChange }) => {
    const [anchorEl, setAnchorEl] = useState(null);

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const handleChange = (newColor) => {
        onColorChange(newColor.hex);
    };

    const handleSave = () => {
        handleClose();
    };

    const open = Boolean(anchorEl);
    const id = open ? 'color-popover' : undefined;

    return (
        <>
            <TextField
                value={color}
                onClick={handleClick}
                style={{ backgroundColor: color }}
            />
            <Popover
                id={id}
                open={open}
                anchorEl={anchorEl}
                onClose={handleClose}
                anchorOrigin={{
                    vertical: 'bottom',
                    horizontal: 'left',
                }}
                transformOrigin={{
                    vertical: 'top',
                    horizontal: 'left',
                }}
            >
                <SketchPicker color={color} onChange={handleChange} />
                <Button onClick={handleSave}>Save</Button>
            </Popover>
        </>
    );
};

export default ColorPicker;