import { Slider, Stack, Typography } from "@mui/material";
import { useState } from "react";

interface Props {
    label: string;
    unit: string;
    value: [number, number, number];
    onValueChange: (newVal: [number, number, number]) => void;
    length: number;
    mult: number;
    max: number;
}
export const PlantSlider: React.FC<Props> = ({
    label,
    unit,
    value: initialValue,
    onValueChange,
    length,
    mult,
    max,
}) => {
    const [value, setValue] = useState<[number, number, number]>(initialValue);
    const change = (newV: [number, number, number]) => {
        setValue(newV);
        onValueChange(newV);
    };
    const indexToLabel = ["min", "opt", "max"];
    const marks = Array.from({ length: length }, (_, i) => ({
        label: `${i * mult}${unit}`,
        value: i * mult,
    }));
    return (
        <>
            <Typography variant="h6">{label}</Typography>
            <Stack direction="row" alignItems="center" px={8} pt={6} pb={2}>
                <Slider
                    min={0}
                    max={max}
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
