"use client";
import { AddButton } from "@/components/AddButton";
import { PlantationCard } from "@/components/PlantationCard";
import { PlantChooser } from "@/components/PlantChooser";
import { postBackend, useBackend, useRedirectNotLogged } from "@/services/backend";
import { Plant, Plantation, PlantationDetails } from "@/types/rest";
import { Box, CircularProgress, Stack, TextField, Typography } from "@mui/material";
import { useState } from "react";

export default function Page() {
    const {
        data: plantationsData,
        isLoading,
        error,
        mutate,
    } = useBackend<{ plantations: Plantation[] }>("/api/plantations");
    const plantations = plantationsData?.plantations;
    const [chosenPlant, setChosenPlant] = useState<Plant | null>(null);
    useRedirectNotLogged();

    return (
        <Stack gap={3}>
            <Typography variant="h5">Hodowle</Typography>
            <AddButton<PlantationDetails>
                onSubmit={(data, close) => {
                    // eslint-disable-next-line @typescript-eslint/no-explicit-any
                    const modData = data as any;
                    modData.plant_id = chosenPlant?.uuid ?? "";
                    mutate(postBackend("/api/plantation", modData).then(() => plantationsData)).then(close);
                }}
            >
                <Stack direction="column" gap={2} py={2}>
                    <TextField name="name" label="nazwa" />
                    <Box>
                        <TextField name="latitude" label="latitude" />
                        <TextField name="longtitude" label="longtitude" />
                    </Box>
                    <PlantChooser plant={chosenPlant} onPlantationChange={setChosenPlant} />
                </Stack>
            </AddButton>
            <Stack gap={2}>
                {isLoading && <CircularProgress />}
                {error && "error"}
                {plantations?.map((plantation) => (
                    <PlantationCard
                        title={plantation.name}
                        key={plantation.uuid}
                        id={plantation.uuid}
                    />
                ))}
            </Stack>
        </Stack>
    );
}
