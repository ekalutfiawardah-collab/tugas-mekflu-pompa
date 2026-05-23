if st.session_state.run:
    for i in range(50):

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')

        # Pompa
        pump = plt.Circle((5, 5), 1.2, color='teal')
        ax.add_patch(pump)
        ax.text(5, 5, "POMPA", ha='center', va='center', color='white')

        # Pipa
        ax.plot([0, 4], [5, 5], linewidth=5)
        ax.plot([5, 5], [6.2, 10], linewidth=5)

        # Animasi air
        speed = debit * 20

        for j in range(5):
            t = (i * speed + j * 2) % 10

            if t < 4:
                ax.plot(t, 5, 'bo')

            if t > 4:
                ax.plot(5, 6 + (t - 4), 'bo')

        placeholder.pyplot(fig)
        plt.close(fig)

        time.sleep(0.05)
        
