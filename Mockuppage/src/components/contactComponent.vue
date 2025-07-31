<template>
    <div class="row justify-center items-center">
        <q-btn
        v-if="!showEmails"
        label="Kontakt"
        @click="showEmails = true"
        color="accent"
        text-color="secondary"
        icon="email"
        unelevated
        size="sm"
        />

        <div v-if="showEmails" class="row items-center flex-center">
            <a
                v-for="(email, index) in decodedEmails"
                :key="email"
                :href="'mailto:' + email"
                class="q-ml-sm text-secondary"
                style="text-decoration: none; font-size: 14px;"
            >
                {{ email }}<span v-if="index < decodedEmails.length - 1">,</span>
            </a>
        </div>
    </div>
</template>

<script setup>
    import { ref, computed } from 'vue';
    const showEmails = ref(false);
    const obfuscatedEmails = ref([
    "7l4a9s2s1e6x3m5e8m0p4e2l7l9a1e6n3g8e5r2x9l7e4i1z6a8x2d5e9",
    "7k4r9i2s1t6i3n5a8x0f4i2s7c9h1e6r3x8l5e2i9z7a4x1d6e8",
    "7n4a9t2h1a6l3y5x8w0i4t2t7x9l1e6i3z8a5x2d9e7"
    ])

    const decodedEmails = computed(() => {
    return obfuscatedEmails.value.map(email => {
        let decoded = email.replace(/\d/g, '');
        let parts = decoded.split('x').filter(part => part.length > 0);
        if (parts.length >= 4) {
        const firstName = parts[0];
        const lastName = parts[1];
        const domain = parts[2];
        const tld = parts[3];
        return `${firstName}.${lastName}@${domain}.${tld}`;
        }
        return email;
    });
    });
</script>