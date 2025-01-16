import { PlantationCard } from "@/components/PlantationCard";
import { useBackend } from "@/services/backend";
import { Plantation } from "@/types/rest";
import { CircularProgress, Stack, Typography } from "@mui/material";

export default function Page() {
    const { data: plantations, isLoading, error } = useBackend<Plantation[]>("/api/plantations");
    return (
        <Stack gap={3}>
            <Typography variant="h5">Hodowle</Typography>
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
