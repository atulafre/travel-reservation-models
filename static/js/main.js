// ...existing code...
// This file is copied from src/main.js. See README.md for update instructions.
const app = Vue.createApp({
  data() {
    return {
      rooms: [],
      reservations: [],
      newReservation: {
        roomId: '',
        guestName: '',
        checkIn: '',
        checkOut: ''
      },
      error: '',
      success: ''
    };
  },
  methods: {
    async fetchRooms() {
      const res = await fetch('/api/rooms');
      this.rooms = await res.json();
    },
    async fetchReservations() {
      const res = await fetch('/api/reservations');
      this.reservations = await res.json();
    },
    async makeReservation() {
      this.error = '';
      this.success = '';
      try {
        const res = await fetch('/api/reservations', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.newReservation)
        });
        if (!res.ok) {
          const err = await res.json();
          this.error = err.description || 'Reservation failed.';
        } else {
          this.success = 'Reservation successful!';
          this.fetchRooms();
          this.fetchReservations();
        }
      } catch (e) {
        this.error = 'Network error.';
      }
    },
    async cancelReservation(id) {
      this.error = '';
      this.success = '';
      try {
        const res = await fetch(`/api/reservations/${id}`, { method: 'DELETE' });
        if (!res.ok) {
          const err = await res.json();
          this.error = err.description || 'Cancellation failed.';
        } else {
          this.success = 'Reservation cancelled.';
          this.fetchRooms();
          this.fetchReservations();
        }
      } catch (e) {
        this.error = 'Network error.';
      }
    }
  },
  mounted() {
    this.fetchRooms();
    this.fetchReservations();
  }
});
app.mount('#app');
