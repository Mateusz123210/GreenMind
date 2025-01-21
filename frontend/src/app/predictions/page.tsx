"use client";
import { PlantationChooser } from "@/components/PlantationChooser";
import { useBackend, useRedirectNotLogged, useSSE } from "@/services/backend";
import { Plantation, PredictionInfo, WateringReturnedInfo } from "@/types/rest";
import { Paper, Stack, Typography } from "@mui/material";
import { useMemo, useState } from "react";

export default function Page() {
    const [chosenPlantation, setChosenPlantation] = useState<Plantation | null>(null);
    const plantation = chosenPlantation?.uuid;
    const plantationQueryParams = useMemo(() => ({ plantationUUID: plantation }), [plantation]);
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const data1 = useSSE<PredictionInfo>(
        "/api/predictions",
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        plantationQueryParams as any,
        !Boolean(plantation)
    );
    const prediction =
        data1?.predicted_watering_time &&
        new Date(data1?.predicted_watering_time).toLocaleString("pl-PL");

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const wateringDataRes = useBackend<WateringReturnedInfo>(
        "/api/water",
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        plantationQueryParams as any,
        !Boolean(plantation)
    );
    useRedirectNotLogged();
    const wateringData = wateringDataRes.data?.wateringInfo;

    return (
        <Stack gap={3}>
            <Typography variant="h5" component="h2">
                Predykcje
            </Typography>
            <PlantationChooser
                plantation={chosenPlantation}
                onPlantationChange={setChosenPlantation}
            />
            {chosenPlantation && (
                <>
                    <Paper sx={{ p: 2 }}>
                        <Typography variant="h6">Wyliczony czas optymalnego podlania</Typography>
                        <Typography>{prediction || "Brak danych"}</Typography>
                    </Paper>
                    <Paper sx={{ p: 2 }}>
                        <Typography variant="h6">Historia podlań</Typography>
                        {wateringData &&
                            wateringData.map((watering, i) => (
                                <div key={i}>
                                    {watering[0]}ml -{" "}
                                    {new Date(watering[1] * 1000).toLocaleString("pl-PL")}
                                </div>
                            ))}
                    </Paper>
                </>
            )}
        </Stack>
    );
}
