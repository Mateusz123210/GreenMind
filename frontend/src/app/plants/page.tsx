"use client";
import { AddButton } from "@/components/AddButton";
import { PlantCard } from "@/components/PlantCard";
import { jsonFetcher, postBackend } from "@/services/backend";
import { Plant } from "@/types/rest";
import { Box, Button, LinearProgress, Stack, TextField, Typography } from "@mui/material";
import useSWR from "swr";

export default function Page() {
    const { data: plantsRes, isLoading, mutate } = useSWR<{plants: Plant[]}>("/api/plants", jsonFetcher);
    const plants = plantsRes?.plants
    console.log("plant:")
    console.log(plants)
    return (
        <Stack gap={3}>
            <Typography variant="h5">Rośliny</Typography>
            <AddButton<{ name: string; comments: string }>
                onSubmit={(data) => {
                    const newObject = Object.assign(data, {
                        min_temperature: 0,
                        opt_temperature: 10,
                        max_temperature: 20,
                        min_moisture: 0,
                        opt_moisture: 10,
                        max_moisture: 20,
                        min_illuminance: 0,
                        opt_illuminance: 10,
                        max_illuminance: 20,
                    });

                    mutate(postBackend("/api/plant", newObject) as any, {
                        optimisticData: { plants: [
                            ...plants!,
                            Object.assign(data, {
                                uuid: Math.random() + "",
                                description: data.comments,
                            }),
                        ]},
                    });
                }}
            >
                <Box>
                    <TextField label="Nazwa" name="name" />
                </Box>
                <Box>
                    <TextField label="Uwagi" name="comments" />
                </Box>
            </AddButton>
            <Stack gap={2}>
                {isLoading && <LinearProgress />}
                {plants instanceof Array && plants?.map((plant) => (
                    <PlantCard
                        id={plant.uuid}
                        key={plant.uuid}
                        title={plant.name}
                    />
                ))}
            </Stack>
        </Stack>
    );
}
