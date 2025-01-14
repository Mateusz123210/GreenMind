'use client'
import { Paper, Typography } from "@mui/material";
import { LineChart } from "@mui/x-charts";

interface Props {
    color: string;
    data: number[];
    xAxis: string[];
    label: string;
}
export const Graph: React.FC<Props> = ({color,data,xAxis, label}) => {
    
    return (
        <Paper sx={{ p: 2 }}>
            <Typography variant="h6">{label}</Typography>
            <LineChart
                xAxis={[{data: xAxis, scaleType: "band"}]}
                series={[{ label: label, color, area: true, data: data }]}
                height={300}
                slotProps={{
                    legend: {
                        position: { vertical: "bottom", horizontal: "middle" },
                    },
                }}
            />
        </Paper>
    );
};
