"use client";
import { useBackend, useSSE } from "@/services/backend";
import { PredictionInfo, WateringReturnedInfo } from "@/types/rest";
import { Paper, Stack, Typography } from "@mui/material";
import { useMemo } from "react";

export default function Page() {
    const plantation = "1735683658.5245671485665a807c7-5986-4338-920e-7eba0cfd9528";
    const plantationQueryParams = useMemo(() => ({plantationUUID: plantation}), [plantation])
    const data1 = useSSE<PredictionInfo>("/api/predictions", plantationQueryParams);
    const prediction =
        data1?.predicted_watering_time &&
        new Date(data1?.predicted_watering_time).toLocaleString("pl-PL");

    const wateringDataRes = useBackend<WateringReturnedInfo>("/api/water", plantationQueryParams);
    const wateringData = wateringDataRes.data?.wateringInfo;

    return (
        <Stack gap={3}>
            <Typography variant="h5" component="h2">
                Predykcje
            </Typography>
            <Paper sx={{ p: 2 }}>
                <Typography variant="h6">Wyliczony czas optymalnego podlania</Typography>
                <Typography>{prediction}</Typography>
            </Paper>
            <Paper sx={{ p: 2 }}>
                <Typography variant="h6">Tu przedstawię dane o podlewaniu do tej pory</Typography>
                {wateringData &&
                    wateringData.map((watering, i) => (
                        <div key={i}>
                            {watering[0]} - {new Date(watering[1]).toLocaleString("pl-PL")}
                        </div>
                    ))}
            </Paper>
        </Stack>
    );
}
