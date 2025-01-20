"use client";
import { AddButton } from "@/components/AddButton";
import { PlantationCard } from "@/components/PlantationCard";
import { PlantChooser } from "@/components/PlantChooser";
import { postBackend, useBackend } from "@/services/backend";
import { Plant, Plantation, PlantationDetails } from "@/types/rest";
import { CircularProgress, Stack, TextField, Typography } from "@mui/material";
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

    return (
        <Stack gap={3}>
            <Typography variant="h5">Hodowle</Typography>
            <AddButton<PlantationDetails>
                onSubmit={(data) => {
                    // eslint-disable-next-line @typescript-eslint/no-explicit-any
                    const modData = data as any
                    modData.plant_id = chosenPlant?.name ?? ''
                    mutate(postBackend("/api/plantation", modData).then(() => plantationsData));
                }}
            >
                <Stack direction="column" gap={3}>
                    <TextField name="name" label="nazwa" />
                    <TextField name="latitude" label="latitude" />
                    <TextField name="longitude" label="longitude" />
                    <TextField name="token" label="token" />
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
