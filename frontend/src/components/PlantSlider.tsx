import { Slider, Stack, Typography } from "@mui/material";
import { useState } from "react";


interface Props {
    label: string;
    unit: string;
    value: [number, number, number];
    onValueChange: (newVal: [number, number, number]) => void
}
export const PlantSlider: React.FC<Props> = ({ label, unit, value: initialValue, onValueChange }) => {
    const [value, setValue] = useState<[number, number, number]>(initialValue)
    const change = (newV: [number, number, number]) => {
        setValue(newV)
        onValueChange(newV)
    }
    const indexToLabel = ["min", "opt", "max"];
    const marks = Array.from({ length: 13 }, (_, i) => ({
        label: `${i * 5}${unit}`,
        value: i * 5,
    }));
    return (
        <>
            <Typography variant="h6">{label}</Typography>
            <Stack direction="row" alignItems="center" px={8} pt={6} pb={2}>
                <Slider
                    min={0}
                    max={60}
                    marks={marks}
                    value={value}
                    onChange={(_, newValue) => change(newValue as [number, number, number])}
                    disableSwap
                    valueLabelDisplay="on"
                    valueLabelFormat={(val, i) => `${indexToLabel[i]}: ${val}${unit}`}
                />
            </Stack>
        </>
    );
};
