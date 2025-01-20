"use client";
import { AddButton } from "@/components/AddButton";
import { PlantationCard } from "@/components/PlantationCard";
import { postBackend, useBackend } from "@/services/backend";
import { Plantation, PlantationDetails } from "@/types/rest";
import { CircularProgress, Stack, TextField, Typography } from "@mui/material";

export default function Page() {
    const {
        data: plantationsData,
        isLoading,
        error,
        mutate,
    } = useBackend<{ plantations: Plantation[] }>("/api/plantations");
    const plantations = plantationsData?.plantations;
    return (
        <Stack gap={3}>
            <Typography variant="h5">Hodowle</Typography>
            <AddButton<PlantationDetails>
                onSubmit={(data) => {
                    mutate(postBackend("/api/plantation", data).then(() => plantationsData));
                }}
            >
                <Stack direction="column" gap={3}>
                    <TextField name="name" label="nazwa" />
                    <TextField name="latitude" label="latitude" />
                    <TextField name="longitude" label="longitude" />
                    <TextField name="token" label="token" />
                    <TextField name="plant_id" label="roślina"/>
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
